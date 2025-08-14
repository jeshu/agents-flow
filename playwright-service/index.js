const express = require('express');
const { chromium } = require('playwright');

const app = express();
app.use(express.json());

app.post('/test', async (req, res) => {
  const { url, actions } = req.body;

  if (!url || !actions) {
    return res.status(400).send({ error: 'URL and actions are required' });
  }

  let browser;
  try {
    browser = await chromium.launch();
    const page = await browser.newPage();
    await page.goto(url);

    for (const action of actions) {
      switch (action.type) {
        case 'click':
          await page.click(action.selector);
          break;
        case 'type':
          await page.type(action.selector, action.text);
          break;
        case 'screenshot':
          await page.screenshot({ path: action.path });
          break;
      }
    }

    res.send({ success: true });
  } catch (error) {
    res.status(500).send({ error: error.message });
  } finally {
    if (browser) {
      await browser.close();
    }
  }
});

app.listen(3002, () => {
  console.log('Playwright service listening on port 3002');
});

