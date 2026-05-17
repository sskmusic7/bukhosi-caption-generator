exports.handler = async (event, context) => {
  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const { imageData, style, customPrompt } = JSON.parse(event.body);

    // Get API key from environment variable
    const apiKey = process.env.GEMINI_API_KEY;

    if (!apiKey) {
      return {
        statusCode: 500,
        body: JSON.stringify({ error: 'API key not configured' })
      };
    }

    // Enhancement prompt templates
    const PROMPT_TEMPLATES = {
      professional_studio: `PROFESSIONAL PRODUCT PHOTOGRAPHY TASK:
Create a clean, studio-quality image of this subject.
- Clean white or subtle gradient background
- Soft, even lighting with subtle shadows for depth
- Sharp focus, crisp details visible
- Professional e-commerce aesthetic like Nike.com or Amazon
- Keep the main subject exactly as shown, but enhance the photography quality`,

      contextual_scenery: `CONTEXTUAL LIFESTYLE PHOTOGRAPHY TASK:
Enhance this photo with appropriate setting that matches the content.
- Analyze the subject (person, wine bottle, food, etc.)
- Create complementary environment (vineyard, cellar, tasting room, etc.)
- Natural lighting appropriate to setting
- Maintain authentic atmosphere while elevating quality
- Keep the main subject as shown, add professional context`,

      luxury_editorial: `HIGH-FASHION EDITORIAL PHOTOGRAPHY TASK:
Create a luxury, editorial-quality image.
- Dramatic lighting with depth and contrast
- Sophisticated composition
- Premium aesthetic suitable for fashion magazines
- Elevated, aspirational quality
- Keep the main subject, apply magazine-grade photography techniques`
    };

    // Use custom prompt if provided, otherwise use style template
    const prompt = customPrompt || PROMPT_TEMPLATES[style] || PROMPT_TEMPLATES.professional_studio;

    // Call Imagen 3 API for image-to-image enhancement
    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predictImageGeneration?key=${apiKey}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: prompt + '\n\nGenerate an enhanced, professional version of this image.',
          inputImage: {
            imageBytes: imageData
          },
          numberOfImages: 1,
          aspectRatio: '1:1',
          safetyFilterLevel: 'block_some',
          personGeneration: 'allow_adult'
        })
      }
    );

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Imagen API Error Response:', errorText);
      return {
        statusCode: response.status,
        body: JSON.stringify({ error: `API request failed: ${errorText}` })
      };
    }

    let data;
    try {
      data = await response.json();
    } catch (jsonError) {
      const responseText = await response.text();
      console.error('Failed to parse JSON. Raw response:', responseText);
      return {
        statusCode: 500,
        body: JSON.stringify({ error: `Failed to parse API response: ${responseText}` })
      };
    }

    // Extract generated image from Imagen API response
    const generatedImage = data.predictedImage?.bytesBase64Encoded;

    if (!generatedImage) {
      // If no image was generated, return error details
      console.error('Imagen API Response:', JSON.stringify(data, null, 2));
      return {
        statusCode: 200,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Allow-Methods': 'POST, OPTIONS'
        },
        body: JSON.stringify({
          success: false,
          enhancedImage: null,
          message: 'No image generated from Imagen API. Response: ' + JSON.stringify(data),
          style: style
        })
      };
    }

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
      },
      body: JSON.stringify({
        success: true,
        enhancedImage: generatedImage,
        style: style,
        message: 'Image enhanced successfully'
      })
    };

  } catch (error) {
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
      },
      body: JSON.stringify({ error: error.message })
    };
  }
};