import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
    define: {'process.env': {}},
    plugins: [vue()],
    resolve: {alias: {'vue': 'vue/dist/vue.esm-bundler.js'}},
    base: "/TuringTest/",
    // build: {
    //     rollupOptions: {
    //         external: [
    //             "index.css"
    //         ],
    //
    //     }
    // }
})
