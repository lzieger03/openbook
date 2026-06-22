// Load the admin bundle as an ES module to avoid leaking globals into classic scripts.
import("./bundle.js").catch((error) => {
    console.error("Failed to load OpenBook admin bundle", error);
});
