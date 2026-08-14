// @ts-check
import { defineConfig } from 'astro/config';

// GitHub Pages 프로젝트 사이트 배포 경로 (https://oliverne.github.io/twilight-struggle-kr-patch/)
export default defineConfig({
  site: 'https://oliverne.github.io',
  base: '/twilight-struggle-kr-patch/',
  output: 'static',
  build: {
    inlineStylesheets: 'auto',
  },
});
