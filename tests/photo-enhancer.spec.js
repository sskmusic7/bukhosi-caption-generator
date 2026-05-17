const { test, expect } = require('@playwright/test');

// Test for Photo Enhancer functionality
test.describe('Bukhosi Photo Enhancer Debug', () => {
  const baseUrl = 'https://bukhosi-caption-generator.netlify.app';

  test('should load photo enhancer page', async ({ page }) => {
    await page.goto(`${baseUrl}/photo_enhancer.html`);

    // Wait for page to load
    await page.waitForLoadState('networkidle');

    // Check if the page title is correct
    await expect(page).toHaveTitle(/Photo Enhancer/);

    // Check if the enhancement settings panel is visible
    await expect(page.locator('.card h2').first()).toContainText('Enhancement Settings');

    // Check if upload zone is visible
    await expect(page.locator('.upload-zone')).toBeVisible();

    // Check if enhance button is disabled initially
    await expect(page.locator('#enhanceBtn')).toBeDisabled();

    console.log('✅ Photo enhancer page loaded successfully');
  });

  test('should test API endpoint with sample image', async ({ request }) => {
    // Create a minimal base64 test image (1x1 red pixel)
    const testImageData = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==';

    const response = await request.post(`${baseUrl}/.netlify/functions/enhance-image`, {
      headers: { 'Content-Type': 'application/json' },
      data: {
        imageData: testImageData,
        style: 'professional_studio',
        customPrompt: ''
      }
    });

    const statusCode = response.status();
    const body = await response.json();

    console.log('API Response Status:', statusCode);
    console.log('API Response Body:', JSON.stringify(body, null, 2));

    // The API might return 200 with a message about image generation not being supported
    // or it might return an error
    if (statusCode === 200 && body.success) {
      if (body.enhancementInstructions) {
        console.log('⚠️  Image generation not supported - got instructions instead');
        console.log('Instructions:', body.enhancementInstructions);
      } else if (body.enhancedImage) {
        console.log('✅ Image enhancement worked!');
      }
    } else if (statusCode !== 200) {
      console.log('❌ API returned error:', body.error || body.message);
    }
  });

  test('should test image upload and enhancement flow', async ({ page }) => {
    await page.goto(`${baseUrl}/photo_enhancer.html`);
    await page.waitForLoadState('networkidle');

    // Enable console log capture
    const consoleMessages = [];
    page.on('console', msg => {
      consoleMessages.push(msg.text());
      console.log('Browser Console:', msg.text());
    });

    // Enable network request/response capture
    const apiRequests = [];
    page.on('request', request => {
      if (request.url().includes('/enhance-image')) {
        console.log('API Request URL:', request.url());
        console.log('API Request Method:', request.method());
        apiRequests.push({ url: request.url(), method: request.method() });
      }
    });

    page.on('response', async response => {
      if (response.url().includes('/enhance-image')) {
        const status = response.status();
        console.log('API Response Status:', status);

        try {
          const body = await response.json();
          console.log('API Response Body:', JSON.stringify(body, null, 2));
        } catch (e) {
          console.log('API Response is not JSON:', await response.text());
        }
      }
    });

    // Select a style
    await page.click('.style-option[data-style="professional_studio"]');

    // Select 1 variation
    await page.click('.variation-btn[data-variations="1"]');

    // Create a test image file
    const testImageBuffer = Buffer.from(
      'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==',
      'base64'
    );

    // Upload the image
    const fileInput = page.locator('#imageInput');
    await fileInput.setInputFiles({
      name: 'test.png',
      mimeType: 'image/png',
      buffer: testImageBuffer
    });

    // Wait for image to appear in preview
    await expect(page.locator('.preview-item')).toBeVisible({ timeout: 5000 });

    // Check if enhance button is now enabled
    await expect(page.locator('#enhanceBtn')).toBeEnabled();

    // Click enhance button
    await page.click('#enhanceBtn');

    // Wait for some processing (up to 30 seconds)
    await page.waitForTimeout(5000);

    // Check results
    const progressItems = page.locator('.progress-item');
    const progressCount = await progressItems.count();

    console.log(`✅ Progress items created: ${progressCount}`);

    if (progressCount > 0) {
      const statusText = await progressItems.first().locator('.progress-status').textContent();
      console.log('Status:', statusText);

      // Check for any error messages in console
      const errorMessages = consoleMessages.filter(msg =>
        msg.toLowerCase().includes('error') ||
        msg.toLowerCase().includes('failed') ||
        msg.toLowerCase().includes('cannot')
      );

      if (errorMessages.length > 0) {
        console.log('❌ Console errors detected:', errorMessages);
      }
    }

    // Take a screenshot for debugging
    await page.screenshot({ path: 'debug-enhancer.png', fullPage: true });
    console.log('✅ Screenshot saved to debug-enhancer.png');
  });
});