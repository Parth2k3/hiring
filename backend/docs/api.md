# API Documentation {#api-documentation}

<div class="section-content">
  <h2>Overview</h2>
  <p>This document provides detailed information about the FAQ Management System API endpoints, request/response formats, and authentication methods.</p>
</div>

## Base URL {#base-url}

<div class="code-block">
  <pre><code>http://localhost:8000/api/</code></pre>
</div>


## API Endpoints {#api-endpoints}

### 1. FAQ Endpoints {#faq-endpoints}

#### List FAQs {#list-faqs}

<div class="endpoint-block">
  <pre><code class="language-http">GET /api/faqs/</code></pre>
</div>

<div class="parameters">
  <h4>Query Parameters:</h4>
  <ul>
    <li><code>lang</code> (optional): Language code (e.g., 'es', 'fr', 'hi')</li>
    <li><code>page</code> (optional): Page number for pagination</li>
    <li><code>page_size</code> (optional): Number of items per page (default: 10)</li>
  </ul>
</div>

<div class="response">
  <h4>Response:</h4>
  <pre><code class="language-json">
{
    "count": 10,
    "next": "http://localhost:8000/api/faqs/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "question": "What is this?",
            "answer": "This is a test answer",
            "available_languages": {
                "en": "English",
                "es": "Spanish"
            }
        }
    ]
}
  </code></pre>
</div>

#### Get Single FAQ {#get-single-faq}

<div class="endpoint-block">
  <pre><code class="language-http">GET /api/faqs/{id}/</code></pre>
</div>

<div class="parameters">
  <h4>Parameters:</h4>
  <ul>
    <li><code>id</code>: FAQ ID (path parameter)</li>
    <li><code>lang</code>: Language code (query parameter)</li>
  </ul>
</div>

<div class="response">
  <h4>Response:</h4>
  <pre><code class="language-json">
{
    "id": 1,
    "question": "What is this?",
    "answer": "This is a test answer",
    "available_languages": {
        "en": "English",
        "es": "Spanish"
    }
}
  </code></pre>
</div>

#### Create FAQ {#create-faq}

<div class="endpoint-block">
  <pre><code class="language-http">POST /api/faqs/</code></pre>
</div>

<div class="request">
  <h4>Request Body:</h4>
  <pre><code class="language-json">
{
    "question": "New question?",
    "answer": "New answer"
}
  </code></pre>
</div>

#### Update FAQ {#update-faq}

<div class="endpoint-block">
  <pre><code class="language-http">PUT /api/faqs/{id}/</code></pre>
</div>

<div class="request">
  <h4>Request Body:</h4>
  <pre><code class="language-json">
{
    "question": "Updated question?",
    "answer": "Updated answer"
}
  </code></pre>
</div>

#### Delete FAQ {#delete-faq}

<div class="endpoint-block">
  <pre><code class="language-http">DELETE /api/faqs/{id}/</code></pre>
</div>

#### Request Translation {#request-translation}

<div class="endpoint-block">
  <pre><code class="language-http">POST /api/faqs/{id}/translate/</code></pre>
</div>

<div class="request">
  <h4>Request Body:</h4>
  <pre><code class="language-json">
{
    "language": "es"
}
  </code></pre>
</div>

## Error Handling {#error-handling}

<div class="section-content">
  <p>The API uses standard HTTP response codes:</p>
  <ul>
    <li>200: Success</li>
    <li>201: Created</li>
    <li>400: Bad Request</li>
    <li>401: Unauthorized</li>
    <li>403: Forbidden</li>
    <li>404: Not Found</li>
    <li>500: Internal Server Error</li>
  </ul>
</div>

<div class="error-response">
  <h4>Error Response Format:</h4>
  <pre><code class="language-json">
{
    "error": "Error message",
    "status": 400
}
  </code></pre>
</div>

## Examples {#examples}

### cURL Examples {#curl-examples}

<div class="example-block">
  <h4>1. List FAQs in Spanish:</h4>
  <pre><code class="language-bash">curl http://localhost:8000/api/faqs/?lang=es</code></pre>

  <h4>2. Create new FAQ:</h4>
  <pre><code class="language-bash">
curl -X POST http://localhost:8000/api/faqs/ \
  -H "Content-Type: application/json" \
  -d '{"question": "New question?", "answer": "New answer"}'
  </code></pre>

  <h4>3. Request Translation:</h4>
  <pre><code class="language-bash">
curl -X POST http://localhost:8000/api/faqs/1/translate/ \
  -H "Content-Type: application/json" \
  -d '{"language": "fr"}'
  </code></pre>
</div>


<style>
.section-content {
  margin: 20px 0;
}

.code-block {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 5px;
  margin: 10px 0;
}

.endpoint-block {
  background-color: #e8f5e9;
  padding: 10px;
  border-radius: 5px;
  margin: 10px 0;
}

.parameters, .response, .request {
  margin: 15px 0;
}

.error-response {
  background-color: #ffebee;
  padding: 15px;
  border-radius: 5px;
  margin: 10px 0;
}

.example-block {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 5px;
  margin: 15px 0;
}

pre {
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
}

code {
  font-family: 'Courier New', Courier, monospace;
}
</style>