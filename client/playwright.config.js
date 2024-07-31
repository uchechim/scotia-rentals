//configuration file for Playwright to specify browsers and other settings.

import {defineConfig, devices} from '@playwright/test';

//30 sec, 2 retries, no GUI, retry w/vid on re-ran failed test cases, cross test on chromium, firefox, & webkit (safari e.t.c) browsers
export default defineConfig({
    timeout: 30000,
    retries: 2,
    use:{
        headless: true,
        screenshot: 'only-on-failure',
        video: 'retry-with-video',
    },
    projects:[
        {
            name: 'Chromium',
            use: { ...devices['Desktop Chrome'] },  
        },
        {
            name: 'Firefox',
            use:{...devices['Desktop Firefox']}
        },
        {
            name: 'WebKit',
            use:{...devices['Desktop Safari']}
        }
    ]
})