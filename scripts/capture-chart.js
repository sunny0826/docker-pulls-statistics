const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ 
    headless: "new",  // 使用新版无头模式（puppeteer v20+ 推荐）
    args: ['--no-sandbox']  // 避免 macOS 权限问题
  });
  const page = await browser.newPage();
  
  // 导航到页面并等待网络空闲（最多等待 30 秒）
  await page.goto('https://sunny0826.github.io/docker-pulls-statistics/', { 
    waitUntil: 'networkidle2',
    timeout: 30000 
  });

  // 显式等待图表 canvas 元素加载完成（关键修复）
  await page.waitForSelector('#pullsChart', { timeout: 10000 });

  // 调整截图尺寸（根据页面实际内容高度）
  const contentHeight = await page.evaluate(() => document.body.scrollHeight);
  await page.screenshot({ 
    path: 'docs/chart-preview.png',
    clip: { x: 0, y: 0, width: 800, height: contentHeight }  // 精确裁剪内容区域
  });

  await browser.close();
})();