# COS registration server API

```{warning}
**Beta Notice**: {{COS_ROB}} is currently in `beta`. 
Content and features may change, and some functionality may be incomplete or experimental. 
Feedback is welcome as we continue to improve.
```

The `cos-registration-server` exposes a public API.
The API potential usages are:

- Devices can register, upload dashboards etc.
- Operators can manipulate the database to modify a device, dashboard etc.
- The `cos-registration-server-k8s` uses the API to retrieve data later shared with [integrations](https://documentation.ubuntu.com/juju/latest/reference/relation/index.html).

The use of the API is only recommended from outside of Juju.
Within Juju,
[`cos-registration-server-k8s` integrations](https://charmhub.io/cos-registration-server-k8s/integrations) are recommended.

## API endpoints

<link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui.css" ></link>
<div id="swagger-ui"></div>

<script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-bundle.js" charset="UTF-8" crossorigin> </script>
<script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-standalone-preset.js" charset="UTF-8 crossorigin"> </script>
<script>
window.onload = function() {
  // Begin Swagger UI call region
  const ui = SwaggerUIBundle({
    url: "https://raw.githubusercontent.com/canonical/cos-registration-server/refs/heads/feat/api_documentation/cos_registration_server/openapi.yaml",
    dom_id: '#swagger-ui',
    deepLinking: true,
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ],
    plugins: [],
    validatorUrl: "none",
    defaultModelsExpandDepth: -1,
    supportedSubmitMethods: []
  })
  // End Swagger UI call region

  window.ui = ui

  function addSwaggerTagsToTOC(tags) {
    // Find the last H2 entry in the TOC and insert a 'ul' element for the tag list
    const tocContainer = document.querySelector(
      ".toc-tree > ul > li > ul > li:last-child"
    );
    const tocList = document.createElement("ul");
    tocContainer.appendChild(tocList);
    // Add a link for each tag inside the 'ul' element
    for (const tag of tags) {
      // Create an 'a' element for the tag link
      const tocLink = document.createElement("a");
      tocLink.classList.add("reference", "internal");
      const urlFriendlyTag = tag.replace(/ /g, "-");
      tocLink.href = `#/${urlFriendlyTag}`;
      tocLink.innerText = tag;
      tocLink.addEventListener("click", event => {
        if (event.shiftKey || event.ctrlKey || event.altKey || event.metaKey) {
          return;
        }
        // When the tag link is clicked with no modifier keys:
        // - Scroll the tag section into view
        // - If the tag section is closed, open it (by simulating a click)
        const operationsTag = tag.replace(/ /g, "_");
        const swaggerHeading = document.getElementById(`operations-tag-${operationsTag}`);
        swaggerHeading.scrollIntoView({
          behavior: "smooth"
        });
        if (swaggerHeading.getAttribute("data-is-open") == "false") {
          swaggerHeading.click();
        }
      });
      // Wrap the tag link in a 'li' element and add it to the tag list
      const tocItem = document.createElement("li");
      tocItem.appendChild(tocLink);
      tocList.appendChild(tocItem);
    }
  }

  // Make sure to match the tags defined in openapi.yaml
  addSwaggerTagsToTOC([
    "changes and tasks",
    "checks",
    "exec",
    "files",
    "health",
    "identities",
    "layers",
    "logs",
    "metrics",
    "notices",
    "plan",
    "services",
    "signals",
    "system info"
  ]);
}
</script>
