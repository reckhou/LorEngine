/**
 * Cloudflare Worker proxy for Anthropic API
 *
 * This is an optional template for using a Cloudflare Worker to proxy API requests
 * instead of exposing your API key in the browser.
 *
 * To use this:
 * 1. Create a Cloudflare Worker at https://workers.cloudflare.com
 * 2. Paste this code into the worker
 * 3. Add your ANTHROPIC_API_KEY as a secret in the Cloudflare dashboard
 * 4. Update the wiki sidebar to call your worker URL instead of api.anthropic.com
 *
 * Free tier: 100,000 requests/day
 */

export default {
  async fetch(request, env) {
    // Only allow POST requests to /api/messages
    if (request.method !== "POST") {
      return new Response("Method not allowed", { status: 405 });
    }

    const url = new URL(request.url);
    if (!url.pathname.startsWith("/api/messages")) {
      return new Response("Not found", { status: 404 });
    }

    // Get the API key from environment
    const apiKey = env.ANTHROPIC_API_KEY;
    if (!apiKey) {
      return new Response("API key not configured", { status: 500 });
    }

    try {
      // Forward the request to Anthropic API
      const anthropicUrl = "https://api.anthropic.com" + url.pathname;
      const response = await fetch(anthropicUrl, {
        method: request.method,
        headers: {
          "Content-Type": "application/json",
          "x-api-key": apiKey,
          "anthropic-version": "2023-06-01",
        },
        body: await request.text(),
      });

      // Return the response with CORS headers
      const responseBody = await response.text();
      return new Response(responseBody, {
        status: response.status,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST",
          "Access-Control-Allow-Headers": "Content-Type",
        },
      });
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), {
        status: 500,
        headers: { "Content-Type": "application/json" },
      });
    }
  },
};
