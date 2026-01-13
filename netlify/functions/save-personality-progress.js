const { Storage } = require('@google-cloud/storage');

exports.handler = async (event, context) => {
  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
      },
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  // Handle CORS preflight
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
      },
      body: ''
    };
  }

  try {
    const { answers, currentIndex, userId = 'thandiwe' } = JSON.parse(event.body);
    
    // Get GCP credentials from environment
    const gcpCredentials = process.env.GCP_CREDENTIALS;
    const bucketName = process.env.GCP_BUCKET_NAME || 'bukhosi-personality-profiles';
    
    if (!gcpCredentials) {
      return {
        statusCode: 500,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ error: 'GCP credentials not configured' })
      };
    }

    // Initialize GCP Storage
    const credentials = JSON.parse(gcpCredentials);
    const storage = new Storage({ credentials });
    const bucket = storage.bucket(bucketName);

    // Create filename with timestamp
    const timestamp = new Date().toISOString().split('T')[0];
    const filename = `${userId}_personality_training_${timestamp}.json`;
    
    // Prepare data to save
    const dataToSave = {
      userId,
      timestamp: new Date().toISOString(),
      currentIndex,
      answers,
      lastSaved: new Date().toISOString()
    };

    // Save to GCP Storage
    const file = bucket.file(filename);
    await file.save(JSON.stringify(dataToSave, null, 2), {
      contentType: 'application/json',
      metadata: {
        cacheControl: 'no-cache'
      }
    });

    // Make file publicly readable (optional, for easier access)
    await file.makePublic();

    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        success: true, 
        message: 'Progress saved successfully',
        filename: filename,
        savedAt: new Date().toISOString()
      })
    };

  } catch (error) {
    console.error('Error saving to GCP:', error);
    return {
      statusCode: 500,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        error: error.message || 'Failed to save progress',
        details: process.env.NETLIFY_DEV ? error.stack : undefined
      })
    };
  }
};
