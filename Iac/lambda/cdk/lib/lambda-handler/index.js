exports.handler = async (event) => {
    // Extract specific properties from the event object
    const { resource, path, httpMethod, headers, queryStringParameters, body } = event;
    const response = {
      resource,
      path,
      httpMethod,
      headers,
      queryStringParameters,
      body,
    };
    return {
      body: JSON.stringify(response, null, 2),
      statusCode: 200,
    };
  };