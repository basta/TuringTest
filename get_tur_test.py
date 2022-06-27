import abc
import json
import random
import traceback
from typing import Optional

import praw
import prawcore.exceptions
import tqdm as tqdm

MAX_TEXT_SIZE = 1000


class Post(abc.ABC):
    title: str
    text: str
    subreddit: str

    @abc.abstractmethod
    def from_reddit_post(self, reddit_post: praw.reddit.Submission):
        ...


class HumanPost(Post):
    @staticmethod
    def from_reddit_post(reddit_post: praw.reddit.Submission):
        human_post = HumanPost()
        human_post.title = reddit_post.title[:MAX_TEXT_SIZE]
        human_post.text = reddit_post.selftext[:MAX_TEXT_SIZE]
        human_post.subreddit = reddit_post.subreddit
        return human_post


class GptPost(Post):
    @staticmethod
    def from_reddit_post(reddit_post: praw.reddit.Submission):
        gpt_post = GptPost()
        gpt_post.title = reddit_post.title[:MAX_TEXT_SIZE]
        gpt_post.text = reddit_post.selftext[:MAX_TEXT_SIZE]
        gpt_post.subreddit = GptPost.sub_from_author(reddit_post.author)
        return gpt_post

    @staticmethod
    def sub_from_author(author: praw.reddit.Redditor) -> str:
        return author.name.lower().replace("_", "").split("gpt")[0]


class TurTest:
    human_post: HumanPost
    gpt_post: GptPost
    subreddit: str

    @staticmethod
    def from_gpt_post(gpt_post: GptPost) -> Optional["TurTest"]:
        """
        Creates a turtest from gptpost and a random hot post in the corresponding human subreddit.

        Creation can fail, if no human post with text is found

        :param gpt_post:
        :return:
        """
        tur_test = TurTest()
        tur_test.gpt_post = gpt_post
        print(f"Searching the human subreddit {gpt_post.subreddit}")
        human_subreddit = reddit.subreddit(gpt_post.subreddit)

        # Set the test subreddit from the human subreddit, because the .subreddit of GPTPost might have slightly wrong
        # capitalization or sth
        tur_test.subreddit = human_subreddit.display_name
        hot_human_reddit_posts = list(human_subreddit.hot(limit=10))
        random.shuffle(hot_human_reddit_posts)

        # Find hot post that has text
        for reddit_post in hot_human_reddit_posts:
            if reddit_post.selftext and not reddit_post.stickied:
                human_reddit_post = reddit_post
                break
        else:
            return None

        human_post = HumanPost.from_reddit_post(human_reddit_post)
        tur_test.human_post = human_post

        return tur_test

    def __str__(self):
        return f"""
        Subreddit: {self.subreddit}
        AI title: {self.gpt_post.title}
            | {self.gpt_post.text}        
        Human title: {self.human_post.title}
            | {self.human_post.text}        
        """

    def to_dict(self) -> dict:
        return {
            "subreddit": self.subreddit,
            "human": {"title": self.human_post.title, "text": self.human_post.text},
            "ai": {"title": self.gpt_post.title, "text": self.gpt_post.text},
        }


praw_config = json.load(open("praw_config.json"))
reddit = praw.Reddit(
    client_id=praw_config["id"],
    client_secret=praw_config["secret"],
    user_agent=praw_config["agent"],
)

if __name__ == "__main__":
    gpt_reddit_posts = list(reddit.subreddit("SubSimulatorGPT2").hot(limit=1000))
    tur_tests = []
    for gpt_reddit_post in tqdm.tqdm(gpt_reddit_posts):
        if not gpt_reddit_post.selftext:
            continue
        try:
            # Turtest creation can fail
            if turtest := TurTest.from_gpt_post(
                GptPost.from_reddit_post(gpt_reddit_post)
            ):
                tur_tests.append(turtest)

        except (prawcore.exceptions.NotFound, prawcore.exceptions.Redirect):
            print(f"Subreddit for author: {gpt_reddit_post.author} not found")
        except Exception:
            print("Trouble creating tur test")
            traceback.print_exc()
    open("turtests.json", "w+").write(
        json.dumps([tur_test.to_dict() for tur_test in tur_tests])
    )
