// ../../../node_modules/esm-env/dev-fallback.js
var node_env = globalThis.process?.env?.NODE_ENV;
var dev_fallback_default = node_env && !node_env.toLowerCase().startsWith("prod");

// ../../../node_modules/svelte/src/internal/shared/utils.js
var is_array = Array.isArray;
var index_of = Array.prototype.indexOf;
var includes = Array.prototype.includes;
var array_from = Array.from;
var object_keys = Object.keys;
var define_property = Object.defineProperty;
var get_descriptor = Object.getOwnPropertyDescriptor;
var get_descriptors = Object.getOwnPropertyDescriptors;
var object_prototype = Object.prototype;
var array_prototype = Array.prototype;
var get_prototype_of = Object.getPrototypeOf;
var is_extensible = Object.isExtensible;
function is_function(thing) {
  return typeof thing === "function";
}
var noop = () => {
};
function run_all(arr) {
  for (var i = 0; i < arr.length; i++) {
    arr[i]();
  }
}
function deferred() {
  var resolve;
  var reject;
  var promise = new Promise((res, rej) => {
    resolve = res;
    reject = rej;
  });
  return { promise, resolve, reject };
}

// ../../../node_modules/svelte/src/internal/client/constants.js
var DERIVED = 1 << 1;
var EFFECT = 1 << 2;
var RENDER_EFFECT = 1 << 3;
var MANAGED_EFFECT = 1 << 24;
var BLOCK_EFFECT = 1 << 4;
var BRANCH_EFFECT = 1 << 5;
var ROOT_EFFECT = 1 << 6;
var BOUNDARY_EFFECT = 1 << 7;
var CONNECTED = 1 << 9;
var CLEAN = 1 << 10;
var DIRTY = 1 << 11;
var MAYBE_DIRTY = 1 << 12;
var INERT = 1 << 13;
var DESTROYED = 1 << 14;
var REACTION_RAN = 1 << 15;
var DESTROYING = 1 << 25;
var EFFECT_TRANSPARENT = 1 << 16;
var EAGER_EFFECT = 1 << 17;
var HEAD_EFFECT = 1 << 18;
var EFFECT_PRESERVED = 1 << 19;
var USER_EFFECT = 1 << 20;
var EFFECT_OFFSCREEN = 1 << 25;
var WAS_MARKED = 1 << 16;
var REACTION_IS_UPDATING = 1 << 21;
var ASYNC = 1 << 22;
var ERROR_VALUE = 1 << 23;
var STATE_SYMBOL = /* @__PURE__ */ Symbol("$state");
var LEGACY_PROPS = /* @__PURE__ */ Symbol("legacy props");
var LOADING_ATTR_SYMBOL = /* @__PURE__ */ Symbol("");
var PROXY_PATH_SYMBOL = /* @__PURE__ */ Symbol("proxy path");
var ATTRIBUTES_CACHE = /* @__PURE__ */ Symbol("attributes");
var CLASS_CACHE = /* @__PURE__ */ Symbol("class");
var STYLE_CACHE = /* @__PURE__ */ Symbol("style");
var TEXT_CACHE = /* @__PURE__ */ Symbol("text");
var FORM_RESET_HANDLER = /* @__PURE__ */ Symbol("form reset");
var HMR_ANCHOR = /* @__PURE__ */ Symbol("hmr anchor");
var STALE_REACTION = new class StaleReactionError extends Error {
  name = "StaleReactionError";
  message = "The reaction that called `getAbortSignal()` was re-run or destroyed";
}();
var IS_XHTML = (
  // We gotta write it like this because after downleveling the pure comment may end up in the wrong location
  !!globalThis.document?.contentType && /* @__PURE__ */ globalThis.document.contentType.includes("xml")
);
var TEXT_NODE = 3;
var COMMENT_NODE = 8;

// ../../../node_modules/svelte/src/internal/shared/errors.js
function invariant_violation(message) {
  if (dev_fallback_default) {
    const error = new Error(`invariant_violation
An invariant violation occurred, meaning Svelte's internal assumptions were flawed. This is a bug in Svelte, not your app \u2014 please open an issue at https://github.com/sveltejs/svelte, citing the following message: "${message}"
https://svelte.dev/e/invariant_violation`);
    error.name = "Svelte error";
    throw error;
  } else {
    throw new Error(`https://svelte.dev/e/invariant_violation`);
  }
}
function lifecycle_outside_component(name) {
  if (dev_fallback_default) {
    const error = new Error(`lifecycle_outside_component
\`${name}(...)\` can only be used during component initialisation
https://svelte.dev/e/lifecycle_outside_component`);
    error.name = "Svelte error";
    throw error;
  } else {
    throw new Error(`https://svelte.dev/e/lifecycle_outside_component`);
  }
}

// ../../../node_modules/svelte/src/internal/client/errors.js
function async_derived_orphan() {
  if (dev_fallback_default) {
    const error = new Error(`async_derived_orphan
Cannot create a \`$derived(...)\` with an \`await\` expression outside of an effect tree
https://svelte.dev/e/async_derived_orphan`);
    error.name = "Svelte error";
    throw error;
  } else {
    throw new Error(`https://svelte.dev/e/async_derived_orphan`);
  }
}
function bind_invalid_checkbox_value() {
  if (dev_fallback_default) {
    const error = new Error(`bind_invalid_checkbox_value
Using \`bind:value\` together with a checkbox input is not allowed. Use \`bind:checked\` instead
https://svelte.dev/e/bind_invalid_checkbox_value`);
    error.name = "Svelte error";
    throw error;
  } else {
    throw new Error(`https://svelte.dev/e/bind_invalid_checkbox_value`);
  }
}
function derived_references_self() {
  if (dev_fallback_default) {
    const error = new Error(`derived_references_self
A derived value cannot reference itself recursively
https://svelte.dev/e/derived_references_self`);
    error.name = "Svelte error";
    throw error;
  } else {
    throw new Error(`https://svelte.dev/e/derived_references_self`);
  }
}
function each_key_duplicate(a, b, value) {
  if (dev_fallback_default) {
    const error = new Error(`each_key_duplicate
${value ? `Keyed each block has duplicate key \`${value}\` at indexes ${a} and ${b}` : `Keyed each block has duplicate key at indexes ${a} and ${b}`}
https://svelte.dev/e/each_key_duplicate`);
    error.name = "Svelte error";
    throw error;
  } else {
    throw new Error(`https://svelte.dev/e/each_key_duplicate`);
  }
}
function each_key_volatile(index2, a, b) {
  if (dev_fallback_default) {
    const error = new Error(`each_key_volatile
Keyed each block has key that is not idempotent \u2014 the key for item at index ${index2} was \`${a}\` but is now \`${b}\`. Keys must be the same each time for a given item
https://svelte.dev/e/each_key_volatile`);
    error.name = "Svelte error";
    throw error;
  } else {
    throw new Error(`https://svelte.dev/e/each_key_volatile`);
  }
}
function effect_in_teardown(rune) {
  if (dev_fallback_default) {
    const error = new Error(`effect_in_teardown
\`${rune}\` cannot be used inside an effect cleanup function
https://svelte.dev/e/effect_in_teardown`);
    error.name = "Svelte error";
    throw error;
  } else {
    throw new Error(`https://svelte.dev/e/effect_in_teardown`);
  }
}
function effect_in_unowned_derived() {
  if (dev_fallback_default) {
    const error = new Error(`effect_in_unowned_derived
Effect cannot be created inside a \`$derived\` value that was not itself created inside an effect
https://svelte.dev/e/effect_in_unowned_derived`);
    error.name = "Svelte error";
    throw error;
  } else {
    throw new Error(`https://svelte.dev/e/effect_in_unowned_derived`);
  }
}
function effect_orphan(rune) {
  if (dev_fallback_default) {
    const error = new Error(`effect_orphan
\`${rune}\` can only be used inside an effect (e.g. during component initialisation)
https://svelte.dev/e/effect_orphan`);
    error.name = "Svelte error";
    throw error;
  } else {
    throw new Error(`https://svelte.dev/e/effect_orphan`);
  }
}
function effect_update_depth_exceeded() {
  if (dev_fallback_default) {
    const error = new Error(`effect_update_depth_exceeded
Maximum update depth exceeded. This typically indicates that an effect reads and writes the same piece of state
https://svelte.dev/e/effect_update_depth_exceeded`);
    error.name = "Svelte error";
    throw error;
  } else {
    throw new Error(`https://svelte.dev/e/effect_update_depth_exceeded`);
  }
}
function hydration_failed() {
  if (dev_fallback_default) {
    const error = new Error(`hydration_failed
Failed to hydrate the application
https://svelte.dev/e/hydration_failed`);
    error.name = "Svelte error";
    throw error;
  } else {
    throw new Error(`https://svelte.dev/e/hydration_failed`);
  }
}
function props_invalid_value(key2) {
  if (dev_fallback_default) {
    const error = new Error(`props_invalid_value
Cannot do \`bind:${key2}={undefined}\` when \`${key2}\` has a fallback value
https://svelte.dev/e/props_invalid_value`);
    error.name = "Svelte error";
    throw error;
  } else {
    throw new Error(`https://svelte.dev/e/props_invalid_value`);
  }
}
function rune_outside_svelte(rune) {
  if (dev_fallback_default) {
    const error = new Error(`rune_outside_svelte
The \`${rune}\` rune is only available inside \`.svelte\` and \`.svelte.js/ts\` files
https://svelte.dev/e/rune_outside_svelte`);
    error.name = "Svelte error";
    throw error;
  } else {
    throw new Error(`https://svelte.dev/e/rune_outside_svelte`);
  }
}
function state_descriptors_fixed() {
  if (dev_fallback_default) {
    const error = new Error(`state_descriptors_fixed
Property descriptors defined on \`$state\` objects must contain \`value\` and always be \`enumerable\`, \`configurable\` and \`writable\`.
https://svelte.dev/e/state_descriptors_fixed`);
    error.name = "Svelte error";
    throw error;
  } else {
    throw new Error(`https://svelte.dev/e/state_descriptors_fixed`);
  }
}
function state_prototype_fixed() {
  if (dev_fallback_default) {
    const error = new Error(`state_prototype_fixed
Cannot set prototype of \`$state\` object
https://svelte.dev/e/state_prototype_fixed`);
    error.name = "Svelte error";
    throw error;
  } else {
    throw new Error(`https://svelte.dev/e/state_prototype_fixed`);
  }
}
function state_unsafe_mutation() {
  if (dev_fallback_default) {
    const error = new Error(`state_unsafe_mutation
Updating state inside \`$derived(...)\`, \`$inspect(...)\` or a template expression is forbidden. If the value should not be reactive, declare it without \`$state\`
https://svelte.dev/e/state_unsafe_mutation`);
    error.name = "Svelte error";
    throw error;
  } else {
    throw new Error(`https://svelte.dev/e/state_unsafe_mutation`);
  }
}
function svelte_boundary_reset_onerror() {
  if (dev_fallback_default) {
    const error = new Error(`svelte_boundary_reset_onerror
A \`<svelte:boundary>\` \`reset\` function cannot be called while an error is still being handled
https://svelte.dev/e/svelte_boundary_reset_onerror`);
    error.name = "Svelte error";
    throw error;
  } else {
    throw new Error(`https://svelte.dev/e/svelte_boundary_reset_onerror`);
  }
}

// ../../../node_modules/svelte/src/constants.js
var EACH_ITEM_REACTIVE = 1;
var EACH_INDEX_REACTIVE = 1 << 1;
var EACH_IS_CONTROLLED = 1 << 2;
var EACH_IS_ANIMATED = 1 << 3;
var EACH_ITEM_IMMUTABLE = 1 << 4;
var PROPS_IS_IMMUTABLE = 1;
var PROPS_IS_RUNES = 1 << 1;
var PROPS_IS_UPDATED = 1 << 2;
var PROPS_IS_BINDABLE = 1 << 3;
var PROPS_IS_LAZY_INITIAL = 1 << 4;
var TRANSITION_OUT = 1 << 1;
var TRANSITION_GLOBAL = 1 << 2;
var TEMPLATE_FRAGMENT = 1;
var TEMPLATE_USE_IMPORT_NODE = 1 << 1;
var TEMPLATE_USE_SVG = 1 << 2;
var TEMPLATE_USE_MATHML = 1 << 3;
var HYDRATION_START = "[";
var HYDRATION_START_ELSE = "[!";
var HYDRATION_START_FAILED = "[?";
var HYDRATION_END = "]";
var HYDRATION_ERROR = {};
var ELEMENT_PRESERVE_ATTRIBUTE_CASE = 1 << 1;
var ELEMENT_IS_INPUT = 1 << 2;
var UNINITIALIZED = /* @__PURE__ */ Symbol("uninitialized");
var FILENAME = /* @__PURE__ */ Symbol("filename");
var NAMESPACE_HTML = "http://www.w3.org/1999/xhtml";

// ../../../node_modules/svelte/src/internal/client/warnings.js
var bold = "font-weight: bold";
var normal = "font-weight: normal";
function await_reactivity_loss(name) {
  if (dev_fallback_default) {
    console.warn(`%c[svelte] await_reactivity_loss
%cDetected reactivity loss when reading \`${name}\`. This happens when state is read in an async function after an earlier \`await\`
https://svelte.dev/e/await_reactivity_loss`, bold, normal);
  } else {
    console.warn(`https://svelte.dev/e/await_reactivity_loss`);
  }
}
function await_waterfall(name, location) {
  if (dev_fallback_default) {
    console.warn(`%c[svelte] await_waterfall
%cAn async derived, \`${name}\` (${location}) was not read immediately after it resolved. This often indicates an unnecessary waterfall, which can slow down your app
https://svelte.dev/e/await_waterfall`, bold, normal);
  } else {
    console.warn(`https://svelte.dev/e/await_waterfall`);
  }
}
function derived_inert() {
  if (dev_fallback_default) {
    console.warn(`%c[svelte] derived_inert
%cReading a derived belonging to a now-destroyed effect may result in stale values
https://svelte.dev/e/derived_inert`, bold, normal);
  } else {
    console.warn(`https://svelte.dev/e/derived_inert`);
  }
}
function hydration_attribute_changed(attribute, html2, value) {
  if (dev_fallback_default) {
    console.warn(`%c[svelte] hydration_attribute_changed
%cThe \`${attribute}\` attribute on \`${html2}\` changed its value between server and client renders. The client value, \`${value}\`, will be ignored in favour of the server value
https://svelte.dev/e/hydration_attribute_changed`, bold, normal);
  } else {
    console.warn(`https://svelte.dev/e/hydration_attribute_changed`);
  }
}
function hydration_mismatch(location) {
  if (dev_fallback_default) {
    console.warn(
      `%c[svelte] hydration_mismatch
%c${location ? `Hydration failed because the initial UI does not match what was rendered on the server. The error occurred near ${location}` : "Hydration failed because the initial UI does not match what was rendered on the server"}
https://svelte.dev/e/hydration_mismatch`,
      bold,
      normal
    );
  } else {
    console.warn(`https://svelte.dev/e/hydration_mismatch`);
  }
}
function lifecycle_double_unmount() {
  if (dev_fallback_default) {
    console.warn(`%c[svelte] lifecycle_double_unmount
%cTried to unmount a component that was not mounted
https://svelte.dev/e/lifecycle_double_unmount`, bold, normal);
  } else {
    console.warn(`https://svelte.dev/e/lifecycle_double_unmount`);
  }
}
function state_proxy_equality_mismatch(operator) {
  if (dev_fallback_default) {
    console.warn(`%c[svelte] state_proxy_equality_mismatch
%cReactive \`$state(...)\` proxies and the values they proxy have different identities. Because of this, comparisons with \`${operator}\` will produce unexpected results
https://svelte.dev/e/state_proxy_equality_mismatch`, bold, normal);
  } else {
    console.warn(`https://svelte.dev/e/state_proxy_equality_mismatch`);
  }
}
function state_proxy_unmount() {
  if (dev_fallback_default) {
    console.warn(`%c[svelte] state_proxy_unmount
%cTried to unmount a state proxy, rather than a component
https://svelte.dev/e/state_proxy_unmount`, bold, normal);
  } else {
    console.warn(`https://svelte.dev/e/state_proxy_unmount`);
  }
}
function svelte_boundary_reset_noop() {
  if (dev_fallback_default) {
    console.warn(`%c[svelte] svelte_boundary_reset_noop
%cA \`<svelte:boundary>\` \`reset\` function only resets the boundary the first time it is called
https://svelte.dev/e/svelte_boundary_reset_noop`, bold, normal);
  } else {
    console.warn(`https://svelte.dev/e/svelte_boundary_reset_noop`);
  }
}

// ../../../node_modules/svelte/src/internal/client/dom/hydration.js
var hydrating = false;
function set_hydrating(value) {
  hydrating = value;
}
var hydrate_node;
function set_hydrate_node(node) {
  if (node === null) {
    hydration_mismatch();
    throw HYDRATION_ERROR;
  }
  return hydrate_node = node;
}
function hydrate_next() {
  return set_hydrate_node(get_next_sibling(hydrate_node));
}
function reset(node) {
  if (!hydrating) return;
  if (get_next_sibling(hydrate_node) !== null) {
    hydration_mismatch();
    throw HYDRATION_ERROR;
  }
  hydrate_node = node;
}
function next(count = 1) {
  if (hydrating) {
    var i = count;
    var node = hydrate_node;
    while (i--) {
      node = /** @type {TemplateNode} */
      get_next_sibling(node);
    }
    hydrate_node = node;
  }
}
function skip_nodes(remove = true) {
  var depth = 0;
  var node = hydrate_node;
  while (true) {
    if (node.nodeType === COMMENT_NODE) {
      var data = (
        /** @type {Comment} */
        node.data
      );
      if (data === HYDRATION_END) {
        if (depth === 0) return node;
        depth -= 1;
      } else if (data === HYDRATION_START || data === HYDRATION_START_ELSE || // "[1", "[2", etc. for if blocks
      data[0] === "[" && !isNaN(Number(data.slice(1)))) {
        depth += 1;
      }
    }
    var next2 = (
      /** @type {TemplateNode} */
      get_next_sibling(node)
    );
    if (remove) node.remove();
    node = next2;
  }
}
function read_hydration_instruction(node) {
  if (!node || node.nodeType !== COMMENT_NODE) {
    hydration_mismatch();
    throw HYDRATION_ERROR;
  }
  return (
    /** @type {Comment} */
    node.data
  );
}

// ../../../node_modules/svelte/src/internal/client/reactivity/equality.js
function equals(value) {
  return value === this.v;
}
function safe_not_equal(a, b) {
  return a != a ? b == b : a !== b || a !== null && typeof a === "object" || typeof a === "function";
}
function safe_equals(value) {
  return !safe_not_equal(value, this.v);
}

// ../../../node_modules/svelte/src/internal/flags/index.js
var async_mode_flag = false;
var legacy_mode_flag = false;
var tracing_mode_flag = false;
function enable_async_mode_flag() {
  async_mode_flag = true;
}

// ../../../node_modules/svelte/src/internal/client/dev/tracing.js
var tracing_expressions = null;
function tag(source2, label) {
  source2.label = label;
  tag_proxy(source2.v, label);
  return source2;
}
function tag_proxy(value, label) {
  value?.[PROXY_PATH_SYMBOL]?.(label);
  return value;
}

// ../../../node_modules/svelte/src/internal/shared/dev.js
function get_error(label) {
  const error = new Error();
  const stack2 = get_stack();
  if (stack2.length === 0) {
    return null;
  }
  stack2.unshift("\n");
  define_property(error, "stack", {
    value: stack2.join("\n")
  });
  define_property(error, "name", {
    value: label
  });
  return (
    /** @type {Error & { stack: string }} */
    error
  );
}
function get_stack() {
  const limit = Error.stackTraceLimit;
  Error.stackTraceLimit = Infinity;
  const stack2 = new Error().stack;
  Error.stackTraceLimit = limit;
  if (!stack2) return [];
  const lines = stack2.split("\n");
  const new_lines = [];
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const posixified = line.replaceAll("\\", "/");
    if (line.trim() === "Error") {
      continue;
    }
    if (line.includes("validate_each_keys")) {
      return [];
    }
    if (posixified.includes("svelte/src/internal") || posixified.includes("node_modules/.vite")) {
      continue;
    }
    new_lines.push(line);
  }
  return new_lines;
}
function invariant(condition, message) {
  if (!dev_fallback_default) {
    throw new Error("invariant(...) was not guarded by if (DEV)");
  }
  if (!condition) invariant_violation(message);
}

// ../../../node_modules/svelte/src/internal/client/context.js
var component_context = null;
function set_component_context(context) {
  component_context = context;
}
var dev_stack = null;
function set_dev_stack(stack2) {
  dev_stack = stack2;
}
var dev_current_component_function = null;
function set_dev_current_component_function(fn) {
  dev_current_component_function = fn;
}
function push(props, runes = false, fn) {
  component_context = {
    p: component_context,
    i: false,
    c: null,
    e: null,
    s: props,
    x: null,
    r: (
      /** @type {Effect} */
      active_effect
    ),
    l: legacy_mode_flag && !runes ? { s: null, u: null, $: [] } : null
  };
  if (dev_fallback_default) {
    component_context.function = fn;
    dev_current_component_function = fn;
  }
}
function pop(component2) {
  var context = (
    /** @type {ComponentContext} */
    component_context
  );
  var effects = context.e;
  if (effects !== null) {
    context.e = null;
    for (var fn of effects) {
      create_user_effect(fn);
    }
  }
  if (component2 !== void 0) {
    context.x = component2;
  }
  context.i = true;
  component_context = context.p;
  if (dev_fallback_default) {
    dev_current_component_function = component_context?.function ?? null;
  }
  return component2 ?? /** @type {T} */
  {};
}
function is_runes() {
  return !legacy_mode_flag || component_context !== null && component_context.l === null;
}

// ../../../node_modules/svelte/src/internal/client/dom/task.js
var micro_tasks = [];
function run_micro_tasks() {
  var tasks = micro_tasks;
  micro_tasks = [];
  run_all(tasks);
}
function queue_micro_task(fn) {
  if (micro_tasks.length === 0 && !is_flushing_sync) {
    var tasks = micro_tasks;
    queueMicrotask(() => {
      if (tasks === micro_tasks) run_micro_tasks();
    });
  }
  micro_tasks.push(fn);
}
function flush_tasks() {
  while (micro_tasks.length > 0) {
    run_micro_tasks();
  }
}

// ../../../node_modules/svelte/src/internal/client/error-handling.js
var adjustments = /* @__PURE__ */ new WeakMap();
function handle_error(error) {
  var effect2 = active_effect;
  if (effect2 === null) {
    active_reaction.f |= ERROR_VALUE;
    return error;
  }
  if (dev_fallback_default && error instanceof Error && !adjustments.has(error)) {
    adjustments.set(error, get_adjustments(error, effect2));
  }
  if ((effect2.f & REACTION_RAN) === 0 && (effect2.f & EFFECT) === 0) {
    if (dev_fallback_default && !effect2.parent && error instanceof Error) {
      apply_adjustments(error);
    }
    throw error;
  }
  invoke_error_boundary(error, effect2);
}
function invoke_error_boundary(error, effect2) {
  while (effect2 !== null) {
    if ((effect2.f & BOUNDARY_EFFECT) !== 0) {
      if ((effect2.f & REACTION_RAN) === 0) {
        throw error;
      }
      try {
        effect2.b.error(error);
        return;
      } catch (e) {
        error = e;
      }
    }
    effect2 = effect2.parent;
  }
  if (dev_fallback_default && error instanceof Error) {
    apply_adjustments(error);
  }
  throw error;
}
function get_adjustments(error, effect2) {
  const message_descriptor = get_descriptor(error, "message");
  if (message_descriptor && !message_descriptor.configurable) return;
  var indent = is_firefox ? "  " : "	";
  var component_stack = `
${indent}in ${effect2.fn?.name || "<unknown>"}`;
  var context = effect2.ctx;
  while (context !== null) {
    component_stack += `
${indent}in ${context.function?.[FILENAME].split("/").pop()}`;
    context = context.p;
  }
  return {
    message: error.message + `
${component_stack}
`,
    stack: error.stack?.split("\n").filter((line) => !line.includes("svelte/src/internal")).join("\n")
  };
}
function apply_adjustments(error) {
  const adjusted = adjustments.get(error);
  if (adjusted) {
    define_property(error, "message", {
      value: adjusted.message
    });
    define_property(error, "stack", {
      value: adjusted.stack
    });
  }
}

// ../../../node_modules/svelte/src/internal/client/reactivity/status.js
var STATUS_MASK = ~(DIRTY | MAYBE_DIRTY | CLEAN);
function set_signal_status(signal, status) {
  signal.f = signal.f & STATUS_MASK | status;
}
function update_derived_status(derived3) {
  if ((derived3.f & CONNECTED) !== 0 || derived3.deps === null) {
    set_signal_status(derived3, CLEAN);
  } else {
    set_signal_status(derived3, MAYBE_DIRTY);
  }
}

// ../../../node_modules/svelte/src/internal/client/reactivity/utils.js
function clear_marked(deps) {
  if (deps === null) return;
  for (const dep of deps) {
    if ((dep.f & DERIVED) === 0 || (dep.f & WAS_MARKED) === 0) {
      continue;
    }
    dep.f ^= WAS_MARKED;
    clear_marked(
      /** @type {Derived} */
      dep.deps
    );
  }
}
function defer_effect(effect2, dirty_effects, maybe_dirty_effects) {
  if ((effect2.f & DIRTY) !== 0) {
    dirty_effects.add(effect2);
  } else if ((effect2.f & MAYBE_DIRTY) !== 0) {
    maybe_dirty_effects.add(effect2);
  }
  clear_marked(effect2.deps);
  set_signal_status(effect2, CLEAN);
}

// ../../../node_modules/svelte/src/store/utils.js
function subscribe_to_store(store, run3, invalidate) {
  if (store == null) {
    run3(void 0);
    if (invalidate) invalidate(void 0);
    return noop;
  }
  const unsub = untrack(
    () => store.subscribe(
      run3,
      // @ts-expect-error
      invalidate
    )
  );
  return unsub.unsubscribe ? () => unsub.unsubscribe() : unsub;
}

// ../../../node_modules/svelte/src/store/shared/index.js
var subscriber_queue = [];
function writable(value, start = noop) {
  let stop = null;
  const subscribers = /* @__PURE__ */ new Set();
  function set2(new_value) {
    if (safe_not_equal(value, new_value)) {
      value = new_value;
      if (stop) {
        const run_queue = !subscriber_queue.length;
        for (const subscriber of subscribers) {
          subscriber[1]();
          subscriber_queue.push(subscriber, value);
        }
        if (run_queue) {
          for (let i = 0; i < subscriber_queue.length; i += 2) {
            subscriber_queue[i][0](subscriber_queue[i + 1]);
          }
          subscriber_queue.length = 0;
        }
      }
    }
  }
  function update2(fn) {
    set2(fn(
      /** @type {T} */
      value
    ));
  }
  function subscribe(run3, invalidate = noop) {
    const subscriber = [run3, invalidate];
    subscribers.add(subscriber);
    if (subscribers.size === 1) {
      stop = start(set2, update2) || noop;
    }
    run3(
      /** @type {T} */
      value
    );
    return () => {
      subscribers.delete(subscriber);
      if (subscribers.size === 0 && stop) {
        stop();
        stop = null;
      }
    };
  }
  return { set: set2, update: update2, subscribe };
}
function get(store) {
  let value;
  subscribe_to_store(store, (_) => value = _)();
  return value;
}

// ../../../node_modules/svelte/src/internal/client/reactivity/store.js
var legacy_is_updating_store = false;
var is_store_binding = false;
var IS_UNMOUNTED = /* @__PURE__ */ Symbol("unmounted");
function store_get(store, store_name, stores) {
  const entry = stores[store_name] ??= {
    store: null,
    source: mutable_source(void 0),
    unsubscribe: noop
  };
  if (dev_fallback_default) {
    entry.source.label = store_name;
  }
  if (entry.store !== store && !(IS_UNMOUNTED in stores)) {
    entry.unsubscribe();
    entry.store = store ?? null;
    if (store == null) {
      entry.source.v = void 0;
      entry.unsubscribe = noop;
    } else {
      var is_synchronous_callback = true;
      entry.unsubscribe = subscribe_to_store(store, (v) => {
        if (is_synchronous_callback) {
          entry.source.v = v;
        } else {
          set(entry.source, v);
        }
      });
      is_synchronous_callback = false;
    }
  }
  if (store && IS_UNMOUNTED in stores) {
    return get(store);
  }
  return get2(entry.source);
}
function setup_stores() {
  const stores = {};
  function cleanup() {
    teardown(() => {
      for (var store_name in stores) {
        const ref = stores[store_name];
        ref.unsubscribe();
      }
      define_property(stores, IS_UNMOUNTED, {
        enumerable: false,
        value: true
      });
    });
  }
  return [stores, cleanup];
}
function capture_store_binding(fn) {
  var previous_is_store_binding = is_store_binding;
  try {
    is_store_binding = false;
    return [fn(), is_store_binding];
  } finally {
    is_store_binding = previous_is_store_binding;
  }
}

// ../../../node_modules/svelte/src/internal/client/reactivity/batch.js
var first_batch = null;
var last_batch = null;
var current_batch = null;
var previous_batch = null;
var batch_values = null;
var last_scheduled_effect = null;
var is_flushing_sync = false;
var is_processing = false;
var collected_effects = null;
var legacy_updates = null;
var flush_count = 0;
var source_stacks = /* @__PURE__ */ new Set();
var uid = 1;
var Batch = class _Batch {
  id = uid++;
  /** True as soon as `#process` was called */
  #started = false;
  linked = true;
  /** @type {Batch | null} */
  #prev = null;
  /** @type {Batch | null} */
  #next = null;
  /** @type {Map<Effect, ReturnType<typeof deferred<any>>>} */
  async_deriveds = /* @__PURE__ */ new Map();
  /**
   * The current values of any signals that are updated in this batch.
   * Tuple format: [value, is_derived] (note: is_derived is false for deriveds, too, if they were overridden via assignment)
   * They keys of this map are identical to `this.#previous`
   * @type {Map<Value, [any, boolean]>}
   */
  current = /* @__PURE__ */ new Map();
  /**
   * The values of any signals (sources and deriveds) that are updated in this batch _before_ those updates took place.
   * They keys of this map are identical to `this.#current`
   * @type {Map<Value, any>}
   */
  previous = /* @__PURE__ */ new Map();
  /**
   * When the batch is committed (and the DOM is updated), we need to remove old branches
   * and append new ones by calling the functions added inside (if/each/key/etc) blocks
   * @type {Set<(batch: Batch) => void>}
   */
  #commit_callbacks = /* @__PURE__ */ new Set();
  /**
   * If a fork is discarded, we need to destroy any effects that are no longer needed
   * @type {Set<(batch: Batch) => void>}
   */
  #discard_callbacks = /* @__PURE__ */ new Set();
  /**
   * The number of async effects that are currently in flight
   */
  #pending = 0;
  /**
   * Async effects that are currently in flight, _not_ inside a pending boundary
   * @type {Map<Effect, number>}
   */
  #blocking_pending = /* @__PURE__ */ new Map();
  /**
   * A deferred that resolves when the batch is committed, used with `settled()`
   * TODO replace with Promise.withResolvers once supported widely enough
   * @type {{ promise: Promise<void>, resolve: (value?: any) => void, reject: (reason: unknown) => void } | null}
   */
  #deferred = null;
  /**
   * The root effects that need to be flushed
   * @type {Effect[]}
   */
  #roots = [];
  /**
   * Effects created while this batch was active.
   * @type {Effect[]}
   */
  #new_effects = [];
  /**
   * Deferred effects (which run after async work has completed) that are DIRTY
   * @type {Set<Effect>}
   */
  #dirty_effects = /* @__PURE__ */ new Set();
  /**
   * Deferred effects that are MAYBE_DIRTY
   * @type {Set<Effect>}
   */
  #maybe_dirty_effects = /* @__PURE__ */ new Set();
  /**
   * A map of branches that still exist, but will be destroyed when this batch
   * is committed — we skip over these during `process`.
   * The value contains child effects that were dirty/maybe_dirty before being reset,
   * so they can be rescheduled if the branch survives.
   * @type {Map<Effect, { d: Effect[], m: Effect[] }>}
   */
  #skipped_branches = /* @__PURE__ */ new Map();
  /**
   * Inverse of #skipped_branches which we need to tell prior batches to unskip them when committing
   * @type {Set<Effect>}
   */
  #unskipped_branches = /* @__PURE__ */ new Set();
  is_fork = false;
  #decrement_queued = false;
  constructor() {
    if (last_batch === null) {
      first_batch = last_batch = this;
    } else {
      last_batch.#next = this;
      this.#prev = last_batch;
    }
    last_batch = this;
  }
  #is_deferred() {
    if (this.is_fork) return true;
    for (const effect2 of this.#blocking_pending.keys()) {
      var e = effect2;
      var skipped = false;
      while (e.parent !== null) {
        if (this.#skipped_branches.has(e)) {
          skipped = true;
          break;
        }
        e = e.parent;
      }
      if (!skipped) {
        return true;
      }
    }
    return false;
  }
  /**
   * Add an effect to the #skipped_branches map and reset its children
   * @param {Effect} effect
   */
  skip_effect(effect2) {
    if (!this.#skipped_branches.has(effect2)) {
      this.#skipped_branches.set(effect2, { d: [], m: [] });
    }
    this.#unskipped_branches.delete(effect2);
  }
  /**
   * Remove an effect from the #skipped_branches map and reschedule
   * any tracked dirty/maybe_dirty child effects
   * @param {Effect} effect
   * @param {(e: Effect) => void} callback
   */
  unskip_effect(effect2, callback = (e) => this.schedule(e)) {
    var tracked = this.#skipped_branches.get(effect2);
    if (tracked) {
      this.#skipped_branches.delete(effect2);
      for (var e of tracked.d) {
        set_signal_status(e, DIRTY);
        callback(e);
      }
      for (e of tracked.m) {
        set_signal_status(e, MAYBE_DIRTY);
        callback(e);
      }
    }
    this.#unskipped_branches.add(effect2);
  }
  #process() {
    this.#started = true;
    if (flush_count++ > 1e3) {
      this.#unlink();
      infinite_loop_guard();
    }
    if (dev_fallback_default) {
      for (const value of this.current.keys()) {
        source_stacks.add(value);
      }
    }
    for (const e of this.#dirty_effects) {
      this.#maybe_dirty_effects.delete(e);
      set_signal_status(e, DIRTY);
      this.schedule(e);
    }
    for (const e of this.#maybe_dirty_effects) {
      set_signal_status(e, MAYBE_DIRTY);
      this.schedule(e);
    }
    const roots = this.#roots;
    this.#roots = [];
    this.apply();
    var effects = collected_effects = [];
    var render_effects = [];
    var updates = legacy_updates = [];
    for (const root15 of roots) {
      try {
        this.#traverse(root15, effects, render_effects);
      } catch (e) {
        reset_all(root15);
        if (!this.#is_deferred()) this.discard();
        throw e;
      }
    }
    current_batch = null;
    if (updates.length > 0) {
      var batch = _Batch.ensure();
      for (const e of updates) {
        batch.schedule(e);
      }
    }
    collected_effects = null;
    legacy_updates = null;
    if (this.#is_deferred()) {
      this.#defer_effects(render_effects);
      this.#defer_effects(effects);
      for (const [e, t] of this.#skipped_branches) {
        reset_branch(e, t);
      }
      if (updates.length > 0) {
        /** @type {unknown} */
        current_batch.#process();
      }
      return;
    }
    const earlier_batch = this.#find_earlier_batch();
    if (earlier_batch) {
      this.#defer_effects(render_effects);
      this.#defer_effects(effects);
      earlier_batch.#merge(this);
      return;
    }
    this.#dirty_effects.clear();
    this.#maybe_dirty_effects.clear();
    for (const fn of this.#commit_callbacks) fn(this);
    this.#commit_callbacks.clear();
    previous_batch = this;
    flush_queued_effects(render_effects);
    flush_queued_effects(effects);
    previous_batch = null;
    this.#deferred?.resolve();
    var next_batch = (
      /** @type {Batch | null} */
      /** @type {unknown} */
      current_batch
    );
    if (this.#pending === 0 && (this.#roots.length === 0 || next_batch !== null)) {
      this.#unlink();
      if (async_mode_flag) {
        this.#commit();
        current_batch = next_batch;
      }
    }
    if (this.#roots.length > 0) {
      if (next_batch !== null) {
        const batch2 = next_batch;
        batch2.#roots.push(...this.#roots.filter((r) => !batch2.#roots.includes(r)));
      } else {
        next_batch = this;
      }
    }
    if (next_batch !== null) {
      next_batch.#process();
    }
  }
  /**
   * Traverse the effect tree, executing effects or stashing
   * them for later execution as appropriate
   * @param {Effect} root
   * @param {Effect[]} effects
   * @param {Effect[]} render_effects
   */
  #traverse(root15, effects, render_effects) {
    root15.f ^= CLEAN;
    var effect2 = root15.first;
    while (effect2 !== null) {
      var flags2 = effect2.f;
      var is_branch = (flags2 & (BRANCH_EFFECT | ROOT_EFFECT)) !== 0;
      var is_skippable_branch = is_branch && (flags2 & CLEAN) !== 0;
      var skip = is_skippable_branch || (flags2 & INERT) !== 0 || this.#skipped_branches.has(effect2);
      if (!skip && effect2.fn !== null) {
        if (is_branch) {
          effect2.f ^= CLEAN;
        } else if ((flags2 & EFFECT) !== 0) {
          effects.push(effect2);
        } else if (async_mode_flag && (flags2 & (RENDER_EFFECT | MANAGED_EFFECT)) !== 0) {
          render_effects.push(effect2);
        } else if (is_dirty(effect2)) {
          if ((flags2 & BLOCK_EFFECT) !== 0) this.#maybe_dirty_effects.add(effect2);
          update_effect(effect2);
        }
        var child2 = effect2.first;
        if (child2 !== null) {
          effect2 = child2;
          continue;
        }
      }
      while (effect2 !== null) {
        var next2 = effect2.next;
        if (next2 !== null) {
          effect2 = next2;
          break;
        }
        effect2 = effect2.parent;
      }
    }
  }
  #find_earlier_batch() {
    var batch = this.#prev;
    while (batch !== null) {
      if (!batch.is_fork) {
        for (const [value, [, is_derived]] of this.current) {
          if (batch.current.has(value) && !is_derived) {
            return batch;
          }
        }
      }
      batch = batch.#prev;
    }
    return null;
  }
  /**
   * @param {Batch} batch
   */
  #merge(batch) {
    for (const [source2, value] of batch.current) {
      if (!this.previous.has(source2) && batch.previous.has(source2)) {
        this.previous.set(source2, batch.previous.get(source2));
      }
      this.current.set(source2, value);
    }
    for (const [effect2, deferred2] of batch.async_deriveds) {
      const d = this.async_deriveds.get(effect2);
      if (d) deferred2.promise.then(d.resolve).catch(d.reject);
    }
    this.transfer_effects(batch.#dirty_effects, batch.#maybe_dirty_effects);
    const mark = (value) => {
      var reactions = value.reactions;
      if (reactions === null) return;
      for (const reaction of reactions) {
        var flags2 = reaction.f;
        if ((flags2 & DERIVED) !== 0) {
          mark(
            /** @type {Derived} */
            reaction
          );
        } else {
          var effect2 = (
            /** @type {Effect} */
            reaction
          );
          if (flags2 & (ASYNC | BLOCK_EFFECT) && !this.async_deriveds.has(effect2)) {
            this.#maybe_dirty_effects.delete(effect2);
            set_signal_status(effect2, DIRTY);
            this.schedule(effect2);
          }
        }
      }
    };
    for (const source2 of this.current.keys()) {
      mark(source2);
    }
    this.oncommit(() => batch.discard());
    batch.#unlink();
    current_batch = this;
    this.#process();
  }
  /**
   * @param {Effect[]} effects
   */
  #defer_effects(effects) {
    for (var i = 0; i < effects.length; i += 1) {
      defer_effect(effects[i], this.#dirty_effects, this.#maybe_dirty_effects);
    }
  }
  /**
   * Associate a change to a given source with the current
   * batch, noting its previous and current values
   * @param {Value} source
   * @param {any} value
   * @param {boolean} [is_derived]
   */
  capture(source2, value, is_derived = false) {
    if (source2.v !== UNINITIALIZED && !this.previous.has(source2)) {
      this.previous.set(source2, source2.v);
    }
    if ((source2.f & ERROR_VALUE) === 0) {
      this.current.set(source2, [value, is_derived]);
      batch_values?.set(source2, value);
    }
    if (!this.is_fork) {
      source2.v = value;
    }
  }
  activate() {
    current_batch = this;
  }
  deactivate() {
    current_batch = null;
    batch_values = null;
  }
  flush() {
    try {
      if (dev_fallback_default) {
        source_stacks.clear();
      }
      is_processing = true;
      current_batch = this;
      this.#process();
    } finally {
      flush_count = 0;
      last_scheduled_effect = null;
      collected_effects = null;
      legacy_updates = null;
      is_processing = false;
      current_batch = null;
      batch_values = null;
      old_values.clear();
      if (dev_fallback_default) {
        for (const source2 of source_stacks) {
          source2.updated = null;
        }
      }
    }
  }
  discard() {
    for (const fn of this.#discard_callbacks) fn(this);
    this.#discard_callbacks.clear();
    this.#unlink();
    this.#deferred?.resolve();
  }
  /**
   * @param {Effect} effect
   */
  register_created_effect(effect2) {
    this.#new_effects.push(effect2);
  }
  #commit() {
    for (let batch = first_batch; batch !== null; batch = batch.#next) {
      var is_earlier = batch.id < this.id;
      var sources = [];
      for (const [source3, [value, is_derived]] of this.current) {
        if (batch.current.has(source3)) {
          var batch_value = (
            /** @type {[any, boolean]} */
            batch.current.get(source3)[0]
          );
          if (is_earlier && value !== batch_value) {
            batch.current.set(source3, [value, is_derived]);
          } else {
            continue;
          }
        }
        sources.push(source3);
      }
      if (is_earlier) {
        for (const [effect2, deferred2] of this.async_deriveds) {
          const d = batch.async_deriveds.get(effect2);
          if (d) deferred2.promise.then(d.resolve).catch(d.reject);
        }
      }
      if (!batch.#started) continue;
      var others = [...batch.current.keys()].filter(
        (s) => !/** @type {[any, boolean]} */
        batch.current.get(s)[1] && !this.current.has(s)
      );
      if (others.length === 0) {
        if (is_earlier) {
          batch.discard();
        }
      } else if (sources.length > 0) {
        if (dev_fallback_default && !batch.#decrement_queued) {
          invariant(batch.#roots.length === 0, "Batch has scheduled roots");
        }
        if (is_earlier) {
          for (const unskipped of this.#unskipped_branches) {
            batch.unskip_effect(unskipped, (e) => {
              if ((e.f & (BLOCK_EFFECT | ASYNC)) !== 0) {
                batch.schedule(e);
              } else {
                batch.#defer_effects([e]);
              }
            });
          }
        }
        batch.activate();
        var marked = /* @__PURE__ */ new Set();
        var checked = /* @__PURE__ */ new Map();
        for (var source2 of sources) {
          mark_effects(source2, others, marked, checked);
        }
        checked = /* @__PURE__ */ new Map();
        var current_unequal = [...batch.current].filter(([c, v1]) => {
          const v2 = this.current.get(c);
          if (!v2) return true;
          return v2[0] !== v1[0] || v2[1] !== v1[1];
        }).map(([c]) => c);
        if (current_unequal.length > 0) {
          for (const effect2 of this.#new_effects) {
            if ((effect2.f & (DESTROYED | INERT | EAGER_EFFECT)) === 0 && depends_on(effect2, current_unequal, checked)) {
              if ((effect2.f & (ASYNC | BLOCK_EFFECT)) !== 0) {
                set_signal_status(effect2, DIRTY);
                batch.schedule(effect2);
              } else {
                batch.#dirty_effects.add(effect2);
              }
            }
          }
        }
        if (batch.#roots.length > 0 && !batch.#decrement_queued) {
          batch.apply();
          for (var root15 of batch.#roots) {
            batch.#traverse(root15, [], []);
          }
          batch.#roots = [];
        }
        batch.deactivate();
      }
    }
  }
  /**
   * @param {boolean} blocking
   * @param {Effect} effect
   */
  increment(blocking, effect2) {
    this.#pending += 1;
    if (blocking) {
      let blocking_pending_count = this.#blocking_pending.get(effect2) ?? 0;
      this.#blocking_pending.set(effect2, blocking_pending_count + 1);
    }
  }
  /**
   * @param {boolean} blocking
   * @param {Effect} effect
   */
  decrement(blocking, effect2) {
    this.#pending -= 1;
    if (blocking) {
      let blocking_pending_count = this.#blocking_pending.get(effect2) ?? 0;
      if (blocking_pending_count === 1) {
        this.#blocking_pending.delete(effect2);
      } else {
        this.#blocking_pending.set(effect2, blocking_pending_count - 1);
      }
    }
    if (this.#decrement_queued) return;
    this.#decrement_queued = true;
    queue_micro_task(() => {
      this.#decrement_queued = false;
      if (this.linked) {
        this.flush();
      }
    });
  }
  /**
   * @param {Set<Effect>} dirty_effects
   * @param {Set<Effect>} maybe_dirty_effects
   */
  transfer_effects(dirty_effects, maybe_dirty_effects) {
    for (const e of dirty_effects) {
      this.#dirty_effects.add(e);
    }
    for (const e of maybe_dirty_effects) {
      this.#maybe_dirty_effects.add(e);
    }
    dirty_effects.clear();
    maybe_dirty_effects.clear();
  }
  /** @param {(batch: Batch) => void} fn */
  oncommit(fn) {
    this.#commit_callbacks.add(fn);
  }
  /** @param {(batch: Batch) => void} fn */
  ondiscard(fn) {
    this.#discard_callbacks.add(fn);
  }
  settled() {
    return (this.#deferred ??= deferred()).promise;
  }
  static ensure() {
    if (current_batch === null) {
      const batch = current_batch = new _Batch();
      if (!is_processing && !is_flushing_sync) {
        queue_micro_task(() => {
          if (!batch.#started) {
            batch.flush();
          }
        });
      }
    }
    return current_batch;
  }
  apply() {
    if (!async_mode_flag || !this.is_fork && this.#prev === null && this.#next === null) {
      batch_values = null;
      return;
    }
    batch_values = /* @__PURE__ */ new Map();
    for (const [source2, [value]] of this.current) {
      batch_values.set(source2, value);
    }
    for (let batch = first_batch; batch !== null; batch = batch.#next) {
      if (batch === this || batch.is_fork) continue;
      var intersects = false;
      if (batch.id < this.id) {
        for (const [source2, [, is_derived]] of batch.current) {
          if (is_derived) continue;
          if (this.current.has(source2)) {
            intersects = true;
            break;
          }
        }
      }
      if (!intersects) {
        for (const [source2, previous] of batch.previous) {
          if (!batch_values.has(source2)) {
            batch_values.set(source2, previous);
          }
        }
      }
    }
  }
  /**
   *
   * @param {Effect} effect
   */
  schedule(effect2) {
    last_scheduled_effect = effect2;
    if (effect2.b?.is_pending && (effect2.f & (EFFECT | RENDER_EFFECT | MANAGED_EFFECT)) !== 0 && (effect2.f & REACTION_RAN) === 0) {
      effect2.b.defer_effect(effect2);
      return;
    }
    var e = effect2;
    while (e.parent !== null) {
      e = e.parent;
      var flags2 = e.f;
      if (collected_effects !== null && e === active_effect) {
        if (async_mode_flag) return;
        if ((active_reaction === null || (active_reaction.f & DERIVED) === 0) && !legacy_is_updating_store) {
          return;
        }
      }
      if ((flags2 & (ROOT_EFFECT | BRANCH_EFFECT)) !== 0) {
        if ((flags2 & CLEAN) === 0) {
          return;
        }
        e.f ^= CLEAN;
      }
    }
    this.#roots.push(e);
  }
  #unlink() {
    if (!this.linked) return;
    var prev = this.#prev;
    var next2 = this.#next;
    if (prev === null) {
      first_batch = next2;
    } else {
      prev.#next = next2;
    }
    if (next2 === null) {
      last_batch = prev;
    } else {
      next2.#prev = prev;
    }
    this.linked = false;
  }
};
function flushSync(fn) {
  var was_flushing_sync = is_flushing_sync;
  is_flushing_sync = true;
  try {
    var result;
    if (fn) {
      if (current_batch !== null && !current_batch.is_fork) {
        current_batch.flush();
      }
      result = fn();
    }
    while (true) {
      flush_tasks();
      if (current_batch === null) {
        return (
          /** @type {T} */
          result
        );
      }
      current_batch.flush();
    }
  } finally {
    is_flushing_sync = was_flushing_sync;
  }
}
function infinite_loop_guard() {
  if (dev_fallback_default) {
    var updates = /* @__PURE__ */ new Map();
    for (
      const source2 of
      /** @type {Batch} */
      current_batch.current.keys()
    ) {
      for (const [stack2, update2] of source2.updated ?? []) {
        var entry = updates.get(stack2);
        if (!entry) {
          entry = { error: update2.error, count: 0 };
          updates.set(stack2, entry);
        }
        entry.count += update2.count;
      }
    }
    for (const update2 of updates.values()) {
      if (update2.error) {
        console.error(update2.error);
      }
    }
  }
  try {
    effect_update_depth_exceeded();
  } catch (error) {
    if (dev_fallback_default) {
      define_property(error, "stack", { value: "" });
    }
    invoke_error_boundary(error, last_scheduled_effect);
  }
}
var eager_block_effects = null;
function flush_queued_effects(effects) {
  var length = effects.length;
  if (length === 0) return;
  var i = 0;
  while (i < length) {
    var effect2 = effects[i++];
    if ((effect2.f & (DESTROYED | INERT)) === 0 && is_dirty(effect2)) {
      eager_block_effects = /* @__PURE__ */ new Set();
      update_effect(effect2);
      if (effect2.deps === null && effect2.first === null && effect2.nodes === null && effect2.teardown === null && effect2.ac === null) {
        unlink_effect(effect2);
      }
      if (eager_block_effects?.size > 0) {
        old_values.clear();
        for (const e of eager_block_effects) {
          if ((e.f & (DESTROYED | INERT)) !== 0) continue;
          const ordered_effects = [e];
          let ancestor = e.parent;
          while (ancestor !== null) {
            if (eager_block_effects.has(ancestor)) {
              eager_block_effects.delete(ancestor);
              ordered_effects.push(ancestor);
            }
            ancestor = ancestor.parent;
          }
          for (let j = ordered_effects.length - 1; j >= 0; j--) {
            const e2 = ordered_effects[j];
            if ((e2.f & (DESTROYED | INERT)) !== 0) continue;
            update_effect(e2);
          }
        }
        eager_block_effects.clear();
      }
    }
  }
  eager_block_effects = null;
}
function mark_effects(value, sources, marked, checked) {
  if (marked.has(value)) return;
  marked.add(value);
  if (value.reactions !== null) {
    for (const reaction of value.reactions) {
      const flags2 = reaction.f;
      if ((flags2 & DERIVED) !== 0) {
        mark_effects(
          /** @type {Derived} */
          reaction,
          sources,
          marked,
          checked
        );
      } else if ((flags2 & (ASYNC | BLOCK_EFFECT)) !== 0 && (flags2 & DIRTY) === 0 && depends_on(reaction, sources, checked)) {
        set_signal_status(reaction, DIRTY);
        schedule_effect(
          /** @type {Effect} */
          reaction
        );
      }
    }
  }
}
function depends_on(reaction, sources, checked) {
  const depends = checked.get(reaction);
  if (depends !== void 0) return depends;
  if (reaction.deps !== null) {
    for (const dep of reaction.deps) {
      if (includes.call(sources, dep)) {
        return true;
      }
      if ((dep.f & DERIVED) !== 0 && depends_on(
        /** @type {Derived} */
        dep,
        sources,
        checked
      )) {
        checked.set(
          /** @type {Derived} */
          dep,
          true
        );
        return true;
      }
    }
  }
  checked.set(reaction, false);
  return false;
}
function schedule_effect(effect2) {
  current_batch.schedule(effect2);
}
function reset_branch(effect2, tracked) {
  if ((effect2.f & BRANCH_EFFECT) !== 0 && (effect2.f & CLEAN) !== 0) {
    return;
  }
  if ((effect2.f & DIRTY) !== 0) {
    tracked.d.push(effect2);
  } else if ((effect2.f & MAYBE_DIRTY) !== 0) {
    tracked.m.push(effect2);
  }
  set_signal_status(effect2, CLEAN);
  var e = effect2.first;
  while (e !== null) {
    reset_branch(e, tracked);
    e = e.next;
  }
}
function reset_all(effect2) {
  set_signal_status(effect2, CLEAN);
  var e = effect2.first;
  while (e !== null) {
    reset_all(e);
    e = e.next;
  }
}

// ../../../node_modules/svelte/src/reactivity/create-subscriber.js
function createSubscriber(start) {
  let subscribers = 0;
  let version = source(0);
  let stop;
  if (dev_fallback_default) {
    tag(version, "createSubscriber version");
  }
  return () => {
    if (effect_tracking()) {
      get2(version);
      render_effect(() => {
        if (subscribers === 0) {
          stop = untrack(() => start(() => increment(version)));
        }
        subscribers += 1;
        return () => {
          queue_micro_task(() => {
            subscribers -= 1;
            if (subscribers === 0) {
              stop?.();
              stop = void 0;
              increment(version);
            }
          });
        };
      });
    }
  };
}

// ../../../node_modules/svelte/src/internal/client/dom/blocks/boundary.js
var flags = EFFECT_TRANSPARENT | EFFECT_PRESERVED;
function boundary(node, props, children, transform_error) {
  new Boundary(node, props, children, transform_error);
}
var Boundary = class {
  /** @type {Boundary | null} */
  parent;
  is_pending = false;
  /**
   * API-level transformError transform function. Transforms errors before they reach the `failed` snippet.
   * Inherited from parent boundary, or defaults to identity.
   * @type {(error: unknown) => unknown}
   */
  transform_error;
  /** @type {TemplateNode} */
  #anchor;
  /** @type {TemplateNode | null} */
  #hydrate_open = hydrating ? hydrate_node : null;
  /** @type {BoundaryProps} */
  #props;
  /** @type {((anchor: Node) => void)} */
  #children;
  /** @type {Effect} */
  #effect;
  /** @type {Effect | null} */
  #main_effect = null;
  /** @type {Effect | null} */
  #pending_effect = null;
  /** @type {Effect | null} */
  #failed_effect = null;
  /** @type {DocumentFragment | null} */
  #offscreen_fragment = null;
  #local_pending_count = 0;
  #pending_count = 0;
  #pending_count_update_queued = false;
  /** @type {Set<Effect>} */
  #dirty_effects = /* @__PURE__ */ new Set();
  /** @type {Set<Effect>} */
  #maybe_dirty_effects = /* @__PURE__ */ new Set();
  /**
   * A source containing the number of pending async deriveds/expressions.
   * Only created if `$effect.pending()` is used inside the boundary,
   * otherwise updating the source results in needless `Batch.ensure()`
   * calls followed by no-op flushes
   * @type {Source<number> | null}
   */
  #effect_pending = null;
  #effect_pending_subscriber = createSubscriber(() => {
    this.#effect_pending = source(this.#local_pending_count);
    if (dev_fallback_default) {
      tag(this.#effect_pending, "$effect.pending()");
    }
    return () => {
      this.#effect_pending = null;
    };
  });
  /**
   * @param {TemplateNode} node
   * @param {BoundaryProps} props
   * @param {((anchor: Node) => void)} children
   * @param {((error: unknown) => unknown) | undefined} [transform_error]
   */
  constructor(node, props, children, transform_error) {
    this.#anchor = node;
    this.#props = props;
    this.#children = (anchor) => {
      var effect2 = (
        /** @type {Effect} */
        active_effect
      );
      effect2.b = this;
      effect2.f |= BOUNDARY_EFFECT;
      children(anchor);
    };
    this.parent = /** @type {Effect} */
    active_effect.b;
    this.transform_error = transform_error ?? this.parent?.transform_error ?? ((e) => e);
    this.#effect = block(() => {
      if (hydrating) {
        const comment2 = (
          /** @type {Comment} */
          this.#hydrate_open
        );
        hydrate_next();
        const server_rendered_pending = comment2.data === HYDRATION_START_ELSE;
        const server_rendered_failed = comment2.data.startsWith(HYDRATION_START_FAILED);
        if (server_rendered_failed) {
          const serialized_error = JSON.parse(comment2.data.slice(HYDRATION_START_FAILED.length));
          this.#hydrate_failed_content(serialized_error);
        } else if (server_rendered_pending) {
          this.#hydrate_pending_content();
        } else {
          this.#hydrate_resolved_content();
        }
      } else {
        this.#render();
      }
    }, flags);
    if (hydrating) {
      this.#anchor = hydrate_node;
    }
  }
  #hydrate_resolved_content() {
    try {
      this.#main_effect = branch(() => this.#children(this.#anchor));
    } catch (error) {
      this.error(error);
    }
  }
  /**
   * @param {unknown} error The deserialized error from the server's hydration comment
   */
  #hydrate_failed_content(error) {
    const failed = this.#props.failed;
    if (!failed) return;
    this.#failed_effect = branch(() => {
      failed(
        this.#anchor,
        () => error,
        () => () => {
        }
      );
    });
  }
  #hydrate_pending_content() {
    const pending2 = this.#props.pending;
    if (!pending2) return;
    this.is_pending = true;
    this.#pending_effect = branch(() => pending2(this.#anchor));
    queue_micro_task(() => {
      var fragment = this.#offscreen_fragment = document.createDocumentFragment();
      var anchor = create_text();
      fragment.append(anchor);
      this.#main_effect = this.#run(() => {
        return branch(() => this.#children(anchor));
      });
      if (this.#pending_count === 0) {
        this.#anchor.before(fragment);
        this.#offscreen_fragment = null;
        pause_effect(
          /** @type {Effect} */
          this.#pending_effect,
          () => {
            this.#pending_effect = null;
          }
        );
        this.#resolve(
          /** @type {Batch} */
          current_batch
        );
      }
    });
  }
  #render() {
    try {
      this.is_pending = this.has_pending_snippet();
      this.#pending_count = 0;
      this.#local_pending_count = 0;
      this.#main_effect = branch(() => {
        this.#children(this.#anchor);
      });
      if (this.#pending_count > 0) {
        var fragment = this.#offscreen_fragment = document.createDocumentFragment();
        move_effect(this.#main_effect, fragment);
        const pending2 = (
          /** @type {(anchor: Node) => void} */
          this.#props.pending
        );
        this.#pending_effect = branch(() => pending2(this.#anchor));
      } else {
        this.#resolve(
          /** @type {Batch} */
          current_batch
        );
      }
    } catch (error) {
      this.error(error);
    }
  }
  /**
   * @param {Batch} batch
   */
  #resolve(batch) {
    this.is_pending = false;
    batch.transfer_effects(this.#dirty_effects, this.#maybe_dirty_effects);
  }
  /**
   * Defer an effect inside a pending boundary until the boundary resolves
   * @param {Effect} effect
   */
  defer_effect(effect2) {
    defer_effect(effect2, this.#dirty_effects, this.#maybe_dirty_effects);
  }
  /**
   * Returns `false` if the effect exists inside a boundary whose pending snippet is shown
   * @returns {boolean}
   */
  is_rendered() {
    return !this.is_pending && (!this.parent || this.parent.is_rendered());
  }
  has_pending_snippet() {
    return !!this.#props.pending;
  }
  /**
   * @template T
   * @param {() => T} fn
   */
  #run(fn) {
    var previous_effect = active_effect;
    var previous_reaction = active_reaction;
    var previous_ctx = component_context;
    set_active_effect(this.#effect);
    set_active_reaction(this.#effect);
    set_component_context(this.#effect.ctx);
    try {
      Batch.ensure();
      return fn();
    } catch (e) {
      handle_error(e);
      return null;
    } finally {
      set_active_effect(previous_effect);
      set_active_reaction(previous_reaction);
      set_component_context(previous_ctx);
    }
  }
  /**
   * Updates the pending count associated with the currently visible pending snippet,
   * if any, such that we can replace the snippet with content once work is done
   * @param {1 | -1} d
   * @param {Batch} batch
   */
  #update_pending_count(d, batch) {
    if (!this.has_pending_snippet()) {
      if (this.parent) {
        this.parent.#update_pending_count(d, batch);
      }
      return;
    }
    this.#pending_count += d;
    if (this.#pending_count === 0) {
      this.#resolve(batch);
      if (this.#pending_effect) {
        pause_effect(this.#pending_effect, () => {
          this.#pending_effect = null;
        });
      }
      if (this.#offscreen_fragment) {
        this.#anchor.before(this.#offscreen_fragment);
        this.#offscreen_fragment = null;
      }
    }
  }
  /**
   * Update the source that powers `$effect.pending()` inside this boundary,
   * and controls when the current `pending` snippet (if any) is removed.
   * Do not call from inside the class
   * @param {1 | -1} d
   * @param {Batch} batch
   */
  update_pending_count(d, batch) {
    this.#update_pending_count(d, batch);
    this.#local_pending_count += d;
    if (!this.#effect_pending || this.#pending_count_update_queued) return;
    this.#pending_count_update_queued = true;
    queue_micro_task(() => {
      this.#pending_count_update_queued = false;
      if (this.#effect_pending) {
        internal_set(this.#effect_pending, this.#local_pending_count);
      }
    });
  }
  get_effect_pending() {
    this.#effect_pending_subscriber();
    return get2(
      /** @type {Source<number>} */
      this.#effect_pending
    );
  }
  /** @param {unknown} error */
  error(error) {
    if (!this.#props.onerror && !this.#props.failed) {
      throw error;
    }
    if (current_batch?.is_fork) {
      if (this.#main_effect) current_batch.skip_effect(this.#main_effect);
      if (this.#pending_effect) current_batch.skip_effect(this.#pending_effect);
      if (this.#failed_effect) current_batch.skip_effect(this.#failed_effect);
      current_batch.oncommit(() => {
        this.#handle_error(error);
      });
    } else {
      this.#handle_error(error);
    }
  }
  /**
   * @param {unknown} error
   */
  #handle_error(error) {
    if (this.#main_effect) {
      destroy_effect(this.#main_effect);
      this.#main_effect = null;
    }
    if (this.#pending_effect) {
      destroy_effect(this.#pending_effect);
      this.#pending_effect = null;
    }
    if (this.#failed_effect) {
      destroy_effect(this.#failed_effect);
      this.#failed_effect = null;
    }
    if (hydrating) {
      set_hydrate_node(
        /** @type {TemplateNode} */
        this.#hydrate_open
      );
      next();
      set_hydrate_node(skip_nodes());
    }
    var onerror = this.#props.onerror;
    let failed = this.#props.failed;
    var did_reset = false;
    var calling_on_error = false;
    const reset2 = () => {
      if (did_reset) {
        svelte_boundary_reset_noop();
        return;
      }
      did_reset = true;
      if (calling_on_error) {
        svelte_boundary_reset_onerror();
      }
      if (this.#failed_effect !== null) {
        pause_effect(this.#failed_effect, () => {
          this.#failed_effect = null;
        });
      }
      this.#run(() => {
        this.#render();
      });
    };
    const handle_error_result = (transformed_error) => {
      try {
        calling_on_error = true;
        onerror?.(transformed_error, reset2);
        calling_on_error = false;
      } catch (error2) {
        invoke_error_boundary(error2, this.#effect && this.#effect.parent);
      }
      if (failed) {
        this.#failed_effect = this.#run(() => {
          try {
            return branch(() => {
              var effect2 = (
                /** @type {Effect} */
                active_effect
              );
              effect2.b = this;
              effect2.f |= BOUNDARY_EFFECT;
              failed(
                this.#anchor,
                () => transformed_error,
                () => reset2
              );
            });
          } catch (error2) {
            invoke_error_boundary(
              error2,
              /** @type {Effect} */
              this.#effect.parent
            );
            return null;
          }
        });
      }
    };
    queue_micro_task(() => {
      var result;
      try {
        result = this.transform_error(error);
      } catch (e) {
        invoke_error_boundary(e, this.#effect && this.#effect.parent);
        return;
      }
      if (result !== null && typeof result === "object" && typeof /** @type {any} */
      result.then === "function") {
        result.then(
          handle_error_result,
          /** @param {unknown} e */
          (e) => invoke_error_boundary(e, this.#effect && this.#effect.parent)
        );
      } else {
        handle_error_result(result);
      }
    });
  }
};

// ../../../node_modules/svelte/src/internal/client/reactivity/async.js
function flatten(blockers, sync, async2, fn) {
  const d = is_runes() ? derived : derived_safe_equal;
  var pending2 = blockers.filter((b) => !b.settled);
  var deriveds = sync.map(d);
  if (dev_fallback_default) {
    deriveds.forEach((d2, i) => {
      d2.label = sync[i].toString().replace("() => ", "").replaceAll("$.eager(() => ", "$state.eager(").replace(/\$\.get\((.+?)\)/g, (_, id) => id);
    });
  }
  if (async2.length === 0 && pending2.length === 0) {
    fn(deriveds);
    return;
  }
  var parent = (
    /** @type {Effect} */
    active_effect
  );
  var restore = capture();
  var blocker_promise = pending2.length === 1 ? pending2[0].promise : pending2.length > 1 ? Promise.all(pending2.map((b) => b.promise)) : null;
  function finish(async3) {
    if ((parent.f & DESTROYED) !== 0) {
      return;
    }
    restore();
    try {
      fn([...deriveds, ...async3]);
    } catch (error) {
      invoke_error_boundary(error, parent);
    }
    unset_context();
  }
  var decrement_pending = increment_pending();
  if (async2.length === 0) {
    blocker_promise.then(() => finish([])).finally(decrement_pending);
    return;
  }
  function run3() {
    Promise.all(async2.map((expression) => async_derived(expression))).then(finish).catch((error) => invoke_error_boundary(error, parent)).finally(decrement_pending);
  }
  if (blocker_promise) {
    blocker_promise.then(() => {
      restore();
      run3();
      unset_context();
    });
  } else {
    run3();
  }
}
function capture() {
  var previous_effect = (
    /** @type {Effect} */
    active_effect
  );
  var previous_reaction = active_reaction;
  var previous_component_context = component_context;
  var previous_batch2 = (
    /** @type {Batch} */
    current_batch
  );
  if (dev_fallback_default) {
    var previous_dev_stack = dev_stack;
  }
  return function restore(activate_batch = true) {
    set_active_effect(previous_effect);
    set_active_reaction(previous_reaction);
    set_component_context(previous_component_context);
    if (activate_batch && (previous_effect.f & DESTROYED) === 0) {
      previous_batch2?.activate();
      previous_batch2?.apply();
    }
    if (dev_fallback_default) {
      set_reactivity_loss_tracker(null);
      set_dev_stack(previous_dev_stack);
    }
  };
}
function unset_context(deactivate_batch = true) {
  set_active_effect(null);
  set_active_reaction(null);
  set_component_context(null);
  if (deactivate_batch) current_batch?.deactivate();
  if (dev_fallback_default) {
    set_reactivity_loss_tracker(null);
    set_dev_stack(null);
  }
}
function increment_pending() {
  var effect2 = (
    /** @type {Effect} */
    active_effect
  );
  var boundary2 = effect2.b;
  var batch = (
    /** @type {Batch} */
    current_batch
  );
  var blocking = !!boundary2?.is_rendered();
  boundary2?.update_pending_count(1, batch);
  batch.increment(blocking, effect2);
  return () => {
    boundary2?.update_pending_count(-1, batch);
    batch.decrement(blocking, effect2);
  };
}

// ../../../node_modules/svelte/src/internal/client/reactivity/deriveds.js
var reactivity_loss_tracker = null;
function set_reactivity_loss_tracker(v) {
  reactivity_loss_tracker = v;
}
var recent_async_deriveds = /* @__PURE__ */ new Set();
// @__NO_SIDE_EFFECTS__
function derived(fn) {
  var flags2 = DERIVED | DIRTY;
  if (active_effect !== null) {
    active_effect.f |= EFFECT_PRESERVED;
  }
  const signal = {
    ctx: component_context,
    deps: null,
    effects: null,
    equals,
    f: flags2,
    fn,
    reactions: null,
    rv: 0,
    v: (
      /** @type {V} */
      UNINITIALIZED
    ),
    wv: 0,
    parent: active_effect,
    ac: null
  };
  if (dev_fallback_default && tracing_mode_flag) {
    signal.created = get_error("created at");
  }
  return signal;
}
var OBSOLETE = /* @__PURE__ */ Symbol("obsolete");
// @__NO_SIDE_EFFECTS__
function async_derived(fn, label, location) {
  let parent = (
    /** @type {Effect | null} */
    active_effect
  );
  if (parent === null) {
    async_derived_orphan();
  }
  var promise = (
    /** @type {Promise<V>} */
    /** @type {unknown} */
    void 0
  );
  var signal = source(
    /** @type {V} */
    UNINITIALIZED
  );
  if (dev_fallback_default) signal.label = label ?? fn.toString();
  var should_suspend = !active_reaction;
  var deferreds = /* @__PURE__ */ new Set();
  async_effect(() => {
    var effect2 = (
      /** @type {Effect} */
      active_effect
    );
    if (dev_fallback_default) {
      reactivity_loss_tracker = { effect: effect2, effect_deps: /* @__PURE__ */ new Set(), warned: false };
    }
    var d = deferred();
    promise = d.promise;
    try {
      Promise.resolve(fn()).then(d.resolve, (e) => {
        if (e !== STALE_REACTION) d.reject(e);
      }).finally(unset_context);
    } catch (error) {
      d.reject(error);
      unset_context();
    }
    if (dev_fallback_default) {
      if (reactivity_loss_tracker) {
        if (effect2.deps !== null) {
          for (let i = 0; i < skipped_deps; i += 1) {
            reactivity_loss_tracker.effect_deps.add(effect2.deps[i]);
          }
        }
        if (new_deps !== null) {
          for (let i = 0; i < new_deps.length; i += 1) {
            reactivity_loss_tracker.effect_deps.add(new_deps[i]);
          }
        }
      }
      reactivity_loss_tracker = null;
    }
    var batch = (
      /** @type {Batch} */
      current_batch
    );
    if (should_suspend) {
      if ((effect2.f & REACTION_RAN) !== 0) {
        var decrement_pending = increment_pending();
      }
      if (
        // boundary can be null if the async derived is inside an $effect.root not connected to the component render tree
        parent.b?.is_rendered()
      ) {
        batch.async_deriveds.get(effect2)?.reject(OBSOLETE);
      } else {
        for (const d2 of deferreds.values()) {
          d2.reject(OBSOLETE);
        }
      }
      deferreds.add(d);
      batch.async_deriveds.set(effect2, d);
    }
    const handler = (value, error = void 0) => {
      if (dev_fallback_default) {
        reactivity_loss_tracker = null;
      }
      decrement_pending?.();
      deferreds.delete(d);
      if (error === OBSOLETE) return;
      batch.activate();
      if (error) {
        signal.f |= ERROR_VALUE;
        internal_set(signal, error);
      } else {
        if ((signal.f & ERROR_VALUE) !== 0) {
          signal.f ^= ERROR_VALUE;
        }
        if (dev_fallback_default && location !== void 0 && !signal.equals(value)) {
          recent_async_deriveds.add(signal);
          setTimeout(() => {
            if (recent_async_deriveds.has(signal) && (effect2.f & DESTROYED) === 0) {
              await_waterfall(
                /** @type {string} */
                signal.label,
                location
              );
              recent_async_deriveds.delete(signal);
            }
          });
        }
        internal_set(signal, value);
      }
      batch.deactivate();
    };
    d.promise.then(handler, (e) => handler(null, e || "unknown"));
  });
  teardown(() => {
    for (const d of deferreds) {
      d.reject(OBSOLETE);
    }
  });
  if (dev_fallback_default) {
    signal.f |= ASYNC;
  }
  return new Promise((fulfil) => {
    function next2(p) {
      function go() {
        if (p === promise) {
          fulfil(signal);
        } else {
          next2(promise);
        }
      }
      p.then(go, go);
    }
    next2(promise);
  });
}
// @__NO_SIDE_EFFECTS__
function user_derived(fn) {
  const d = /* @__PURE__ */ derived(fn);
  if (!async_mode_flag) push_reaction_value(d);
  return d;
}
// @__NO_SIDE_EFFECTS__
function derived_safe_equal(fn) {
  const signal = /* @__PURE__ */ derived(fn);
  signal.equals = safe_equals;
  return signal;
}
function destroy_derived_effects(derived3) {
  var effects = derived3.effects;
  if (effects !== null) {
    derived3.effects = null;
    for (var i = 0; i < effects.length; i += 1) {
      destroy_effect(
        /** @type {Effect} */
        effects[i]
      );
    }
  }
}
var stack = [];
function execute_derived(derived3) {
  var value;
  var prev_active_effect = active_effect;
  var parent = derived3.parent;
  if (!is_destroying_effect && parent !== null && derived3.v !== UNINITIALIZED && // if it was never evaluated before, it's guaranteed to fail downstream, so we try to execute instead
  (parent.f & (DESTROYED | INERT)) !== 0) {
    derived_inert();
    return derived3.v;
  }
  set_active_effect(parent);
  if (dev_fallback_default) {
    let prev_eager_effects = eager_effects;
    set_eager_effects(/* @__PURE__ */ new Set());
    try {
      if (includes.call(stack, derived3)) {
        derived_references_self();
      }
      stack.push(derived3);
      derived3.f &= ~WAS_MARKED;
      destroy_derived_effects(derived3);
      value = update_reaction(derived3);
    } finally {
      set_active_effect(prev_active_effect);
      set_eager_effects(prev_eager_effects);
      stack.pop();
    }
  } else {
    try {
      derived3.f &= ~WAS_MARKED;
      destroy_derived_effects(derived3);
      value = update_reaction(derived3);
    } finally {
      set_active_effect(prev_active_effect);
    }
  }
  return value;
}
function update_derived(derived3) {
  var value = execute_derived(derived3);
  if (!derived3.equals(value)) {
    derived3.wv = increment_write_version();
    if (!current_batch?.is_fork || derived3.deps === null) {
      if (current_batch !== null) {
        current_batch.capture(derived3, value, true);
        previous_batch?.capture(derived3, value, true);
      } else {
        derived3.v = value;
      }
      if (derived3.deps === null) {
        set_signal_status(derived3, CLEAN);
        return;
      }
    }
  }
  if (is_destroying_effect) {
    return;
  }
  if (batch_values !== null) {
    if (effect_tracking() || current_batch?.is_fork) {
      batch_values.set(derived3, value);
    }
  } else {
    update_derived_status(derived3);
  }
}
function freeze_derived_effects(derived3) {
  if (derived3.effects === null) return;
  for (const e of derived3.effects) {
    if (e.teardown || e.ac) {
      e.teardown?.();
      e.ac?.abort(STALE_REACTION);
      if (e.fn !== null) e.teardown = noop;
      e.ac = null;
      remove_reactions(e, 0);
      destroy_effect_children(e);
    }
  }
}
function unfreeze_derived_effects(derived3) {
  if (derived3.effects === null) return;
  for (const e of derived3.effects) {
    if (e.teardown && e.fn !== null) {
      update_effect(e);
    }
  }
}

// ../../../node_modules/svelte/src/internal/client/reactivity/sources.js
var eager_effects = /* @__PURE__ */ new Set();
var old_values = /* @__PURE__ */ new Map();
function set_eager_effects(v) {
  eager_effects = v;
}
var eager_effects_deferred = false;
function set_eager_effects_deferred() {
  eager_effects_deferred = true;
}
function source(v, stack2) {
  var signal = {
    f: 0,
    // TODO ideally we could skip this altogether, but it causes type errors
    v,
    reactions: null,
    equals,
    rv: 0,
    wv: 0
  };
  if (dev_fallback_default && tracing_mode_flag) {
    signal.created = stack2 ?? get_error("created at");
    signal.updated = null;
    signal.set_during_effect = false;
    signal.trace = null;
  }
  return signal;
}
// @__NO_SIDE_EFFECTS__
function state(v, stack2) {
  const s = source(v, stack2);
  push_reaction_value(s);
  return s;
}
// @__NO_SIDE_EFFECTS__
function mutable_source(initial_value, immutable = false, trackable = true) {
  const s = source(initial_value);
  if (!immutable) {
    s.equals = safe_equals;
  }
  if (legacy_mode_flag && trackable && component_context !== null && component_context.l !== null) {
    (component_context.l.s ??= []).push(s);
  }
  return s;
}
function set(source2, value, should_proxy = false) {
  if (active_reaction !== null && // since we are untracking the function inside `$inspect.with` we need to add this check
  // to ensure we error if state is set inside an inspect effect
  (!untracking || (active_reaction.f & EAGER_EFFECT) !== 0) && is_runes() && (active_reaction.f & (DERIVED | BLOCK_EFFECT | ASYNC | EAGER_EFFECT)) !== 0 && (current_sources === null || !current_sources.has(source2))) {
    state_unsafe_mutation();
  }
  let new_value = should_proxy ? proxy(value) : value;
  if (dev_fallback_default) {
    tag_proxy(
      new_value,
      /** @type {string} */
      source2.label
    );
  }
  return internal_set(source2, new_value, legacy_updates);
}
function internal_set(source2, value, updated_during_traversal = null) {
  if (!source2.equals(value)) {
    old_values.set(source2, is_destroying_effect ? value : source2.v);
    var batch = Batch.ensure();
    batch.capture(source2, value);
    if (dev_fallback_default) {
      if (tracing_mode_flag || active_effect !== null) {
        source2.updated ??= /* @__PURE__ */ new Map();
        const count = (source2.updated.get("")?.count ?? 0) + 1;
        source2.updated.set("", { error: (
          /** @type {any} */
          null
        ), count });
        if (tracing_mode_flag || count > 5) {
          const error = get_error("updated at");
          if (error !== null) {
            let entry = source2.updated.get(error.stack);
            if (!entry) {
              entry = { error, count: 0 };
              source2.updated.set(error.stack, entry);
            }
            entry.count++;
          }
        }
      }
      if (active_effect !== null) {
        source2.set_during_effect = true;
      }
    }
    if ((source2.f & DERIVED) !== 0) {
      const derived3 = (
        /** @type {Derived} */
        source2
      );
      if ((source2.f & DIRTY) !== 0) {
        execute_derived(derived3);
      }
      if (batch_values === null) {
        update_derived_status(derived3);
      }
    }
    source2.wv = increment_write_version();
    mark_reactions(source2, DIRTY, updated_during_traversal);
    if (is_runes() && active_effect !== null && (active_effect.f & CLEAN) !== 0 && (active_effect.f & (BRANCH_EFFECT | ROOT_EFFECT)) === 0) {
      if (untracked_writes === null) {
        set_untracked_writes([source2]);
      } else {
        untracked_writes.push(source2);
      }
    }
    if (!batch.is_fork && eager_effects.size > 0 && !eager_effects_deferred) {
      flush_eager_effects();
    }
  }
  return value;
}
function flush_eager_effects() {
  eager_effects_deferred = false;
  for (const effect2 of eager_effects) {
    if ((effect2.f & CLEAN) !== 0) {
      set_signal_status(effect2, MAYBE_DIRTY);
    }
    let dirty;
    try {
      dirty = is_dirty(effect2);
    } catch {
      dirty = true;
    }
    if (dirty) {
      update_effect(effect2);
    }
  }
  eager_effects.clear();
}
function increment(source2) {
  set(source2, source2.v + 1);
}
function mark_reactions(signal, status, updated_during_traversal) {
  var reactions = signal.reactions;
  if (reactions === null) return;
  var runes = is_runes();
  var length = reactions.length;
  for (var i = 0; i < length; i++) {
    var reaction = reactions[i];
    var flags2 = reaction.f;
    if (!runes && reaction === active_effect) continue;
    var not_dirty = (flags2 & DIRTY) === 0;
    if (not_dirty) {
      set_signal_status(reaction, status);
    }
    if ((flags2 & EAGER_EFFECT) !== 0) {
      eager_effects.add(
        /** @type {Effect} */
        reaction
      );
    } else if ((flags2 & DERIVED) !== 0) {
      var derived3 = (
        /** @type {Derived} */
        reaction
      );
      batch_values?.delete(derived3);
      if ((flags2 & WAS_MARKED) === 0) {
        if (flags2 & CONNECTED && (active_effect === null || (active_effect.f & REACTION_IS_UPDATING) === 0)) {
          reaction.f |= WAS_MARKED;
        }
        mark_reactions(derived3, MAYBE_DIRTY, updated_during_traversal);
      }
    } else if (not_dirty) {
      var effect2 = (
        /** @type {Effect} */
        reaction
      );
      if ((flags2 & BLOCK_EFFECT) !== 0 && eager_block_effects !== null) {
        eager_block_effects.add(effect2);
      }
      if (updated_during_traversal !== null) {
        updated_during_traversal.push(effect2);
      } else {
        schedule_effect(effect2);
      }
    }
  }
}

// ../../../node_modules/svelte/src/internal/client/proxy.js
var regex_is_valid_identifier = /^[a-zA-Z_$][a-zA-Z_$0-9]*$/;
function proxy(value) {
  if (typeof value !== "object" || value === null || STATE_SYMBOL in value) {
    return value;
  }
  const prototype = get_prototype_of(value);
  if (prototype !== object_prototype && prototype !== array_prototype) {
    return value;
  }
  var sources = /* @__PURE__ */ new Map();
  var is_proxied_array = is_array(value);
  var version = state(0);
  var stack2 = dev_fallback_default && tracing_mode_flag ? get_error("created at") : null;
  var parent_version = update_version;
  var with_parent = (fn) => {
    if (update_version === parent_version) {
      return fn();
    }
    var reaction = active_reaction;
    var version2 = update_version;
    set_active_reaction(null);
    set_update_version(parent_version);
    var result = fn();
    set_active_reaction(reaction);
    set_update_version(version2);
    return result;
  };
  if (is_proxied_array) {
    sources.set("length", state(
      /** @type {any[]} */
      value.length,
      stack2
    ));
    if (dev_fallback_default) {
      value = /** @type {any} */
      inspectable_array(
        /** @type {any[]} */
        value
      );
    }
  }
  var path = "";
  let updating = false;
  function update_path(new_path) {
    if (updating) return;
    updating = true;
    path = new_path;
    tag(version, `${path} version`);
    for (const [prop2, source2] of sources) {
      tag(source2, get_label(path, prop2));
    }
    updating = false;
  }
  return new Proxy(
    /** @type {any} */
    value,
    {
      defineProperty(_, prop2, descriptor) {
        if (!("value" in descriptor) || descriptor.configurable === false || descriptor.enumerable === false || descriptor.writable === false) {
          state_descriptors_fixed();
        }
        var s = sources.get(prop2);
        if (s === void 0) {
          with_parent(() => {
            var s2 = state(descriptor.value, stack2);
            sources.set(prop2, s2);
            if (dev_fallback_default && typeof prop2 === "string") {
              tag(s2, get_label(path, prop2));
            }
            return s2;
          });
        } else {
          set(s, descriptor.value, true);
        }
        return true;
      },
      deleteProperty(target, prop2) {
        var s = sources.get(prop2);
        if (s === void 0) {
          if (prop2 in target) {
            const s2 = with_parent(() => state(UNINITIALIZED, stack2));
            sources.set(prop2, s2);
            increment(version);
            if (dev_fallback_default) {
              tag(s2, get_label(path, prop2));
            }
          }
        } else {
          set(s, UNINITIALIZED);
          increment(version);
        }
        return true;
      },
      get(target, prop2, receiver) {
        if (prop2 === STATE_SYMBOL) {
          return value;
        }
        if (dev_fallback_default && prop2 === PROXY_PATH_SYMBOL) {
          return update_path;
        }
        var s = sources.get(prop2);
        var exists = prop2 in target;
        if (s === void 0 && (!exists || get_descriptor(target, prop2)?.writable)) {
          s = with_parent(() => {
            var p = proxy(exists ? target[prop2] : UNINITIALIZED);
            var s2 = state(p, stack2);
            if (dev_fallback_default) {
              tag(s2, get_label(path, prop2));
            }
            return s2;
          });
          sources.set(prop2, s);
        }
        if (s !== void 0) {
          var v = get2(s);
          return v === UNINITIALIZED ? void 0 : v;
        }
        return Reflect.get(target, prop2, receiver);
      },
      getOwnPropertyDescriptor(target, prop2) {
        var descriptor = Reflect.getOwnPropertyDescriptor(target, prop2);
        if (descriptor && "value" in descriptor) {
          var s = sources.get(prop2);
          if (s) descriptor.value = get2(s);
        } else if (descriptor === void 0) {
          var source2 = sources.get(prop2);
          var value2 = source2?.v;
          if (source2 !== void 0 && value2 !== UNINITIALIZED) {
            return {
              enumerable: true,
              configurable: true,
              value: value2,
              writable: true
            };
          }
        }
        return descriptor;
      },
      has(target, prop2) {
        if (prop2 === STATE_SYMBOL) {
          return true;
        }
        var s = sources.get(prop2);
        var has = s !== void 0 && s.v !== UNINITIALIZED || Reflect.has(target, prop2);
        if (s !== void 0 || active_effect !== null && (!has || get_descriptor(target, prop2)?.writable)) {
          if (s === void 0) {
            s = with_parent(() => {
              var p = has ? proxy(target[prop2]) : UNINITIALIZED;
              var s2 = state(p, stack2);
              if (dev_fallback_default) {
                tag(s2, get_label(path, prop2));
              }
              return s2;
            });
            sources.set(prop2, s);
          }
          var value2 = get2(s);
          if (value2 === UNINITIALIZED) {
            return false;
          }
        }
        return has;
      },
      set(target, prop2, value2, receiver) {
        var s = sources.get(prop2);
        var has = prop2 in target;
        if (is_proxied_array && prop2 === "length") {
          for (var i = value2; i < /** @type {Source<number>} */
          s.v; i += 1) {
            var other_s = sources.get(i + "");
            if (other_s !== void 0) {
              set(other_s, UNINITIALIZED);
            } else if (i in target) {
              other_s = with_parent(() => state(UNINITIALIZED, stack2));
              sources.set(i + "", other_s);
              if (dev_fallback_default) {
                tag(other_s, get_label(path, i));
              }
            }
          }
        }
        if (s === void 0) {
          if (!has || get_descriptor(target, prop2)?.writable) {
            s = with_parent(() => state(void 0, stack2));
            if (dev_fallback_default) {
              tag(s, get_label(path, prop2));
            }
            set(s, proxy(value2));
            sources.set(prop2, s);
          }
        } else {
          has = s.v !== UNINITIALIZED;
          var p = with_parent(() => proxy(value2));
          set(s, p);
        }
        var descriptor = Reflect.getOwnPropertyDescriptor(target, prop2);
        if (descriptor?.set) {
          descriptor.set.call(receiver, value2);
        }
        if (!has) {
          if (is_proxied_array && typeof prop2 === "string") {
            var ls = (
              /** @type {Source<number>} */
              sources.get("length")
            );
            var n = Number(prop2);
            if (Number.isInteger(n) && n >= ls.v) {
              set(ls, n + 1);
            }
          }
          increment(version);
        }
        return true;
      },
      ownKeys(target) {
        get2(version);
        var own_keys = Reflect.ownKeys(target).filter((key3) => {
          var source3 = sources.get(key3);
          return source3 === void 0 || source3.v !== UNINITIALIZED;
        });
        for (var [key2, source2] of sources) {
          if (source2.v !== UNINITIALIZED && !(key2 in target)) {
            own_keys.push(key2);
          }
        }
        return own_keys;
      },
      setPrototypeOf() {
        state_prototype_fixed();
      }
    }
  );
}
function get_label(path, prop2) {
  if (typeof prop2 === "symbol") return `${path}[Symbol(${prop2.description ?? ""})]`;
  if (regex_is_valid_identifier.test(prop2)) return `${path}.${prop2}`;
  return /^\d+$/.test(prop2) ? `${path}[${prop2}]` : `${path}['${prop2}']`;
}
function get_proxied_value(value) {
  try {
    if (value !== null && typeof value === "object" && STATE_SYMBOL in value) {
      return value[STATE_SYMBOL];
    }
  } catch {
  }
  return value;
}
var ARRAY_MUTATING_METHODS = /* @__PURE__ */ new Set([
  "copyWithin",
  "fill",
  "pop",
  "push",
  "reverse",
  "shift",
  "sort",
  "splice",
  "unshift"
]);
function inspectable_array(array) {
  return new Proxy(array, {
    get(target, prop2, receiver) {
      var value = Reflect.get(target, prop2, receiver);
      if (!ARRAY_MUTATING_METHODS.has(
        /** @type {string} */
        prop2
      )) {
        return value;
      }
      return function(...args) {
        set_eager_effects_deferred();
        var result = value.apply(this, args);
        flush_eager_effects();
        return result;
      };
    }
  });
}

// ../../../node_modules/svelte/src/internal/client/dev/equality.js
function init_array_prototype_warnings() {
  const array_prototype2 = Array.prototype;
  const cleanup = Array.__svelte_cleanup;
  if (cleanup) {
    cleanup();
  }
  const { indexOf, lastIndexOf, includes: includes2 } = array_prototype2;
  array_prototype2.indexOf = function(item, from_index) {
    const index2 = indexOf.call(this, item, from_index);
    if (index2 === -1) {
      for (let i = from_index ?? 0; i < this.length; i += 1) {
        if (get_proxied_value(this[i]) === item) {
          state_proxy_equality_mismatch("array.indexOf(...)");
          break;
        }
      }
    }
    return index2;
  };
  array_prototype2.lastIndexOf = function(item, from_index) {
    const index2 = lastIndexOf.call(this, item, from_index ?? this.length - 1);
    if (index2 === -1) {
      for (let i = 0; i <= (from_index ?? this.length - 1); i += 1) {
        if (get_proxied_value(this[i]) === item) {
          state_proxy_equality_mismatch("array.lastIndexOf(...)");
          break;
        }
      }
    }
    return index2;
  };
  array_prototype2.includes = function(item, from_index) {
    const has = includes2.call(this, item, from_index);
    if (!has) {
      for (let i = 0; i < this.length; i += 1) {
        if (get_proxied_value(this[i]) === item) {
          state_proxy_equality_mismatch("array.includes(...)");
          break;
        }
      }
    }
    return has;
  };
  Array.__svelte_cleanup = () => {
    array_prototype2.indexOf = indexOf;
    array_prototype2.lastIndexOf = lastIndexOf;
    array_prototype2.includes = includes2;
  };
}

// ../../../node_modules/svelte/src/internal/client/dom/operations.js
var $window;
var $document;
var is_firefox;
var first_child_getter;
var next_sibling_getter;
function init_operations() {
  if ($window !== void 0) {
    return;
  }
  $window = window;
  $document = document;
  is_firefox = /Firefox/.test(navigator.userAgent);
  var element_prototype = Element.prototype;
  var node_prototype = Node.prototype;
  var text_prototype = Text.prototype;
  first_child_getter = get_descriptor(node_prototype, "firstChild").get;
  next_sibling_getter = get_descriptor(node_prototype, "nextSibling").get;
  if (is_extensible(element_prototype)) {
    element_prototype[CLASS_CACHE] = void 0;
    element_prototype[ATTRIBUTES_CACHE] = null;
    element_prototype[STYLE_CACHE] = void 0;
    element_prototype.__e = void 0;
  }
  if (is_extensible(text_prototype)) {
    text_prototype[TEXT_CACHE] = void 0;
  }
  if (dev_fallback_default) {
    element_prototype.__svelte_meta = null;
    init_array_prototype_warnings();
  }
}
function create_text(value = "") {
  return document.createTextNode(value);
}
// @__NO_SIDE_EFFECTS__
function get_first_child(node) {
  return (
    /** @type {TemplateNode | null} */
    first_child_getter.call(node)
  );
}
// @__NO_SIDE_EFFECTS__
function get_next_sibling(node) {
  return (
    /** @type {TemplateNode | null} */
    next_sibling_getter.call(node)
  );
}
function child(node, is_text) {
  if (!hydrating) {
    return /* @__PURE__ */ get_first_child(node);
  }
  var child2 = /* @__PURE__ */ get_first_child(hydrate_node);
  if (child2 === null) {
    child2 = hydrate_node.appendChild(create_text());
  } else if (is_text && child2.nodeType !== TEXT_NODE) {
    var text2 = create_text();
    child2?.before(text2);
    set_hydrate_node(text2);
    return text2;
  }
  if (is_text) {
    merge_text_nodes(
      /** @type {Text} */
      child2
    );
  }
  set_hydrate_node(child2);
  return child2;
}
function first_child(node, is_text = false) {
  if (!hydrating) {
    var first = /* @__PURE__ */ get_first_child(node);
    if (first instanceof Comment && first.data === "") return /* @__PURE__ */ get_next_sibling(first);
    return first;
  }
  if (is_text) {
    if (hydrate_node?.nodeType !== TEXT_NODE) {
      var text2 = create_text();
      hydrate_node?.before(text2);
      set_hydrate_node(text2);
      return text2;
    }
    merge_text_nodes(
      /** @type {Text} */
      hydrate_node
    );
  }
  return hydrate_node;
}
function sibling(node, count = 1, is_text = false) {
  let next_sibling = hydrating ? hydrate_node : node;
  var last_sibling;
  while (count--) {
    last_sibling = next_sibling;
    next_sibling = /** @type {TemplateNode} */
    /* @__PURE__ */ get_next_sibling(next_sibling);
  }
  if (!hydrating) {
    return next_sibling;
  }
  if (is_text) {
    if (next_sibling?.nodeType !== TEXT_NODE) {
      var text2 = create_text();
      if (next_sibling === null) {
        last_sibling?.after(text2);
      } else {
        next_sibling.before(text2);
      }
      set_hydrate_node(text2);
      return text2;
    }
    merge_text_nodes(
      /** @type {Text} */
      next_sibling
    );
  }
  set_hydrate_node(next_sibling);
  return next_sibling;
}
function clear_text_content(node) {
  node.textContent = "";
}
function should_defer_append() {
  if (!async_mode_flag) return false;
  if (eager_block_effects !== null) return false;
  var flags2 = (
    /** @type {Effect} */
    active_effect.f
  );
  return (flags2 & REACTION_RAN) !== 0;
}
function create_element(tag2, namespace, is2) {
  if (namespace == null || namespace === NAMESPACE_HTML) {
    return (
      /** @type {T extends keyof HTMLElementTagNameMap ? HTMLElementTagNameMap[T] : Element} */
      is2 ? document.createElement(tag2, { is: is2 }) : document.createElement(tag2)
    );
  }
  return (
    /** @type {T extends keyof HTMLElementTagNameMap ? HTMLElementTagNameMap[T] : Element} */
    is2 ? document.createElementNS(namespace, tag2, { is: is2 }) : document.createElementNS(namespace, tag2)
  );
}
function merge_text_nodes(text2) {
  if (
    /** @type {string} */
    text2.nodeValue.length < 65536
  ) {
    return;
  }
  let next2 = text2.nextSibling;
  while (next2 !== null && next2.nodeType === TEXT_NODE) {
    next2.remove();
    text2.nodeValue += /** @type {string} */
    next2.nodeValue;
    next2 = text2.nextSibling;
  }
}

// ../../../node_modules/svelte/src/internal/client/dom/elements/misc.js
function remove_textarea_child(dom) {
  if (hydrating && get_first_child(dom) !== null) {
    clear_text_content(dom);
  }
}
var listening_to_form_reset = false;
function add_form_reset_listener() {
  if (!listening_to_form_reset) {
    listening_to_form_reset = true;
    document.addEventListener(
      "reset",
      (evt) => {
        Promise.resolve().then(() => {
          if (!evt.defaultPrevented) {
            for (
              const e of
              /**@type {HTMLFormElement} */
              evt.target.elements
            ) {
              e[FORM_RESET_HANDLER]?.();
            }
          }
        });
      },
      // In the capture phase to guarantee we get noticed of it (no possibility of stopPropagation)
      { capture: true }
    );
  }
}

// ../../../node_modules/svelte/src/internal/client/dom/elements/bindings/shared.js
function without_reactive_context(fn) {
  var previous_reaction = active_reaction;
  var previous_effect = active_effect;
  set_active_reaction(null);
  set_active_effect(null);
  try {
    return fn();
  } finally {
    set_active_reaction(previous_reaction);
    set_active_effect(previous_effect);
  }
}
function listen_to_event_and_reset_event(element2, event2, handler, on_reset = handler) {
  element2.addEventListener(event2, () => without_reactive_context(handler));
  const prev = (
    /** @type {any} */
    element2[FORM_RESET_HANDLER]
  );
  if (prev) {
    element2[FORM_RESET_HANDLER] = () => {
      prev();
      on_reset(true);
    };
  } else {
    element2[FORM_RESET_HANDLER] = () => on_reset(true);
  }
  add_form_reset_listener();
}

// ../../../node_modules/svelte/src/internal/client/reactivity/effects.js
function validate_effect(rune) {
  if (active_effect === null) {
    if (active_reaction === null) {
      effect_orphan(rune);
    }
    effect_in_unowned_derived();
  }
  if (is_destroying_effect) {
    effect_in_teardown(rune);
  }
}
function push_effect(effect2, parent_effect) {
  var parent_last = parent_effect.last;
  if (parent_last === null) {
    parent_effect.last = parent_effect.first = effect2;
  } else {
    parent_last.next = effect2;
    effect2.prev = parent_last;
    parent_effect.last = effect2;
  }
}
function create_effect(type, fn) {
  var parent = active_effect;
  if (dev_fallback_default) {
    while (parent !== null && (parent.f & EAGER_EFFECT) !== 0) {
      parent = parent.parent;
    }
  }
  if (parent !== null && (parent.f & INERT) !== 0) {
    type |= INERT;
  }
  var effect2 = {
    ctx: component_context,
    deps: null,
    nodes: null,
    f: type | DIRTY | CONNECTED,
    first: null,
    fn,
    last: null,
    next: null,
    parent,
    b: parent && parent.b,
    prev: null,
    teardown: null,
    wv: 0,
    ac: null
  };
  if (dev_fallback_default) {
    effect2.component_function = dev_current_component_function;
  }
  current_batch?.register_created_effect(effect2);
  var e = effect2;
  if ((type & EFFECT) !== 0) {
    if (collected_effects !== null) {
      collected_effects.push(effect2);
    } else {
      Batch.ensure().schedule(effect2);
    }
  } else if (fn !== null) {
    try {
      update_effect(effect2);
    } catch (e2) {
      destroy_effect(effect2);
      throw e2;
    }
    if (e.deps === null && e.teardown === null && e.nodes === null && e.first === e.last && // either `null`, or a singular child
    (e.f & EFFECT_PRESERVED) === 0) {
      e = e.first;
      if ((type & BLOCK_EFFECT) !== 0 && (type & EFFECT_TRANSPARENT) !== 0 && e !== null) {
        e.f |= EFFECT_TRANSPARENT;
      }
    }
  }
  if (e !== null) {
    e.parent = parent;
    if (parent !== null) {
      push_effect(e, parent);
    }
    if (active_reaction !== null && (active_reaction.f & DERIVED) !== 0 && (type & ROOT_EFFECT) === 0) {
      var derived3 = (
        /** @type {Derived} */
        active_reaction
      );
      (derived3.effects ??= []).push(e);
    }
  }
  return effect2;
}
function effect_tracking() {
  return active_reaction !== null && !untracking;
}
function teardown(fn) {
  const effect2 = create_effect(RENDER_EFFECT, null);
  set_signal_status(effect2, CLEAN);
  effect2.teardown = fn;
  return effect2;
}
function user_effect(fn) {
  validate_effect("$effect");
  if (dev_fallback_default) {
    define_property(fn, "name", {
      value: "$effect"
    });
  }
  var flags2 = (
    /** @type {Effect} */
    active_effect.f
  );
  var defer = !active_reaction && (flags2 & BRANCH_EFFECT) !== 0 && component_context !== null && !component_context.i;
  if (defer) {
    var context = (
      /** @type {ComponentContext} */
      component_context
    );
    (context.e ??= []).push(fn);
  } else {
    return create_user_effect(fn);
  }
}
function create_user_effect(fn) {
  return create_effect(EFFECT | USER_EFFECT, fn);
}
function effect_root(fn) {
  Batch.ensure();
  const effect2 = create_effect(ROOT_EFFECT | EFFECT_PRESERVED, fn);
  return () => {
    destroy_effect(effect2);
  };
}
function component_root(fn) {
  Batch.ensure();
  const effect2 = create_effect(ROOT_EFFECT | EFFECT_PRESERVED, fn);
  return (options = {}) => {
    return new Promise((fulfil) => {
      if (options.outro) {
        pause_effect(effect2, () => {
          destroy_effect(effect2);
          fulfil(void 0);
        });
      } else {
        destroy_effect(effect2);
        fulfil(void 0);
      }
    });
  };
}
function effect(fn) {
  return create_effect(EFFECT, fn);
}
function async_effect(fn) {
  return create_effect(ASYNC | EFFECT_PRESERVED, fn);
}
function render_effect(fn, flags2 = 0) {
  return create_effect(RENDER_EFFECT | flags2, fn);
}
function template_effect(fn, sync = [], async2 = [], blockers = []) {
  flatten(blockers, sync, async2, (values) => {
    create_effect(RENDER_EFFECT, () => {
      fn(...values.map(get2));
    });
  });
}
function block(fn, flags2 = 0) {
  var effect2 = create_effect(BLOCK_EFFECT | flags2, fn);
  if (dev_fallback_default) {
    effect2.dev_stack = dev_stack;
  }
  return effect2;
}
function branch(fn) {
  return create_effect(BRANCH_EFFECT | EFFECT_PRESERVED, fn);
}
function execute_effect_teardown(effect2) {
  var teardown2 = effect2.teardown;
  if (teardown2 !== null) {
    const previously_destroying_effect = is_destroying_effect;
    const previous_reaction = active_reaction;
    set_is_destroying_effect(true);
    set_active_reaction(null);
    try {
      teardown2.call(null);
    } finally {
      set_is_destroying_effect(previously_destroying_effect);
      set_active_reaction(previous_reaction);
    }
  }
}
function destroy_effect_children(signal, remove_dom = false) {
  var effect2 = signal.first;
  signal.first = signal.last = null;
  while (effect2 !== null) {
    const controller = effect2.ac;
    if (controller !== null) {
      without_reactive_context(() => {
        controller.abort(STALE_REACTION);
      });
    }
    var next2 = effect2.next;
    if ((effect2.f & ROOT_EFFECT) !== 0) {
      effect2.parent = null;
    } else {
      destroy_effect(effect2, remove_dom);
    }
    effect2 = next2;
  }
}
function destroy_block_effect_children(signal) {
  var effect2 = signal.first;
  while (effect2 !== null) {
    var next2 = effect2.next;
    if ((effect2.f & BRANCH_EFFECT) === 0) {
      destroy_effect(effect2);
    }
    effect2 = next2;
  }
}
function destroy_effect(effect2, remove_dom = true) {
  var removed = false;
  if ((remove_dom || (effect2.f & HEAD_EFFECT) !== 0) && effect2.nodes !== null && effect2.nodes.end !== null) {
    remove_effect_dom(
      effect2.nodes.start,
      /** @type {TemplateNode} */
      effect2.nodes.end
    );
    removed = true;
  }
  effect2.f |= DESTROYING;
  destroy_effect_children(effect2, remove_dom && !removed);
  remove_reactions(effect2, 0);
  var transitions = effect2.nodes && effect2.nodes.t;
  if (transitions !== null) {
    for (const transition2 of transitions) {
      transition2.stop();
    }
  }
  execute_effect_teardown(effect2);
  effect2.f ^= DESTROYING;
  effect2.f |= DESTROYED;
  var parent = effect2.parent;
  if (parent !== null && parent.first !== null) {
    unlink_effect(effect2);
  }
  if (dev_fallback_default) {
    effect2.component_function = null;
  }
  effect2.next = effect2.prev = effect2.teardown = effect2.ctx = effect2.deps = effect2.fn = effect2.nodes = effect2.ac = effect2.b = null;
}
function remove_effect_dom(node, end) {
  while (node !== null) {
    var next2 = node === end ? null : get_next_sibling(node);
    node.remove();
    node = next2;
  }
}
function unlink_effect(effect2) {
  var parent = effect2.parent;
  var prev = effect2.prev;
  var next2 = effect2.next;
  if (prev !== null) prev.next = next2;
  if (next2 !== null) next2.prev = prev;
  if (parent !== null) {
    if (parent.first === effect2) parent.first = next2;
    if (parent.last === effect2) parent.last = prev;
  }
}
function pause_effect(effect2, callback, destroy = true) {
  var transitions = [];
  pause_children(effect2, transitions, true);
  var fn = () => {
    if (destroy) destroy_effect(effect2);
    if (callback) callback();
  };
  var remaining = transitions.length;
  if (remaining > 0) {
    var check = () => --remaining || fn();
    for (var transition2 of transitions) {
      transition2.out(check);
    }
  } else {
    fn();
  }
}
function pause_children(effect2, transitions, local) {
  if ((effect2.f & INERT) !== 0) return;
  effect2.f ^= INERT;
  var t = effect2.nodes && effect2.nodes.t;
  if (t !== null) {
    for (const transition2 of t) {
      if (transition2.is_global || local) {
        transitions.push(transition2);
      }
    }
  }
  var child2 = effect2.first;
  while (child2 !== null) {
    var sibling2 = child2.next;
    if ((child2.f & ROOT_EFFECT) === 0) {
      var transparent = (child2.f & EFFECT_TRANSPARENT) !== 0 || // If this is a branch effect without a block effect parent,
      // it means the parent block effect was pruned. In that case,
      // transparency information was transferred to the branch effect.
      (child2.f & BRANCH_EFFECT) !== 0 && (effect2.f & BLOCK_EFFECT) !== 0;
      pause_children(child2, transitions, transparent ? local : false);
    }
    child2 = sibling2;
  }
}
function resume_effect(effect2) {
  resume_children(effect2, true);
}
function resume_children(effect2, local) {
  if ((effect2.f & INERT) === 0) return;
  effect2.f ^= INERT;
  if ((effect2.f & CLEAN) === 0) {
    set_signal_status(effect2, DIRTY);
    Batch.ensure().schedule(effect2);
  }
  var child2 = effect2.first;
  while (child2 !== null) {
    var sibling2 = child2.next;
    var transparent = (child2.f & EFFECT_TRANSPARENT) !== 0 || (child2.f & BRANCH_EFFECT) !== 0;
    resume_children(child2, transparent ? local : false);
    child2 = sibling2;
  }
  var t = effect2.nodes && effect2.nodes.t;
  if (t !== null) {
    for (const transition2 of t) {
      if (transition2.is_global || local) {
        transition2.in();
      }
    }
  }
}
function move_effect(effect2, fragment) {
  if (!effect2.nodes) return;
  var node = effect2.nodes.start;
  var end = effect2.nodes.end;
  while (node !== null) {
    var next2 = node === end ? null : get_next_sibling(node);
    fragment.append(node);
    node = next2;
  }
}

// ../../../node_modules/svelte/src/internal/client/legacy.js
var captured_signals = null;

// ../../../node_modules/svelte/src/internal/client/runtime.js
var is_updating_effect = false;
var is_destroying_effect = false;
function set_is_destroying_effect(value) {
  is_destroying_effect = value;
}
var active_reaction = null;
var untracking = false;
function set_active_reaction(reaction) {
  active_reaction = reaction;
}
var active_effect = null;
function set_active_effect(effect2) {
  active_effect = effect2;
}
var current_sources = null;
function push_reaction_value(value) {
  if (active_reaction !== null && (!async_mode_flag || (active_reaction.f & DERIVED) !== 0)) {
    (current_sources ??= /* @__PURE__ */ new Set()).add(value);
  }
}
var new_deps = null;
var skipped_deps = 0;
var untracked_writes = null;
function set_untracked_writes(value) {
  untracked_writes = value;
}
var write_version = 1;
var read_version = 0;
var update_version = read_version;
function set_update_version(value) {
  update_version = value;
}
function increment_write_version() {
  return ++write_version;
}
function is_dirty(reaction) {
  var flags2 = reaction.f;
  if ((flags2 & DIRTY) !== 0) {
    return true;
  }
  if (flags2 & DERIVED) {
    reaction.f &= ~WAS_MARKED;
  }
  if ((flags2 & MAYBE_DIRTY) !== 0) {
    var dependencies = (
      /** @type {Value[]} */
      reaction.deps
    );
    var length = dependencies.length;
    for (var i = 0; i < length; i++) {
      var dependency = dependencies[i];
      if (is_dirty(
        /** @type {Derived} */
        dependency
      )) {
        update_derived(
          /** @type {Derived} */
          dependency
        );
      }
      if (dependency.wv > reaction.wv) {
        return true;
      }
    }
    if ((flags2 & CONNECTED) !== 0 && // During time traveling we don't want to reset the status so that
    // traversal of the graph in the other batches still happens
    batch_values === null) {
      set_signal_status(reaction, CLEAN);
    }
  }
  return false;
}
function schedule_possible_effect_self_invalidation(signal, effect2, root15 = true) {
  var reactions = signal.reactions;
  if (reactions === null) return;
  if (!async_mode_flag && current_sources !== null && current_sources.has(signal)) {
    return;
  }
  for (var i = 0; i < reactions.length; i++) {
    var reaction = reactions[i];
    if ((reaction.f & DERIVED) !== 0) {
      schedule_possible_effect_self_invalidation(
        /** @type {Derived} */
        reaction,
        effect2,
        false
      );
    } else if (effect2 === reaction) {
      if (root15) {
        set_signal_status(reaction, DIRTY);
      } else if ((reaction.f & CLEAN) !== 0) {
        set_signal_status(reaction, MAYBE_DIRTY);
      }
      schedule_effect(
        /** @type {Effect} */
        reaction
      );
    }
  }
}
function update_reaction(reaction) {
  var previous_deps = new_deps;
  var previous_skipped_deps = skipped_deps;
  var previous_untracked_writes = untracked_writes;
  var previous_reaction = active_reaction;
  var previous_sources = current_sources;
  var previous_component_context = component_context;
  var previous_untracking = untracking;
  var previous_update_version = update_version;
  var flags2 = reaction.f;
  new_deps = /** @type {null | Value[]} */
  null;
  skipped_deps = 0;
  untracked_writes = null;
  active_reaction = (flags2 & (BRANCH_EFFECT | ROOT_EFFECT)) === 0 ? reaction : null;
  current_sources = null;
  set_component_context(reaction.ctx);
  untracking = false;
  update_version = ++read_version;
  if (reaction.ac !== null) {
    without_reactive_context(() => {
      reaction.ac.abort(STALE_REACTION);
    });
    reaction.ac = null;
  }
  try {
    reaction.f |= REACTION_IS_UPDATING;
    var fn = (
      /** @type {Function} */
      reaction.fn
    );
    var result = fn();
    reaction.f |= REACTION_RAN;
    var deps = reaction.deps;
    var is_fork = current_batch?.is_fork;
    if (new_deps !== null) {
      var i;
      if (!is_fork) {
        remove_reactions(reaction, skipped_deps);
      }
      if (deps !== null && skipped_deps > 0) {
        deps.length = skipped_deps + new_deps.length;
        for (i = 0; i < new_deps.length; i++) {
          deps[skipped_deps + i] = new_deps[i];
        }
      } else {
        reaction.deps = deps = new_deps;
      }
      if (effect_tracking() && (reaction.f & CONNECTED) !== 0) {
        for (i = skipped_deps; i < deps.length; i++) {
          (deps[i].reactions ??= []).push(reaction);
        }
      }
    } else if (!is_fork && deps !== null && skipped_deps < deps.length) {
      remove_reactions(reaction, skipped_deps);
      deps.length = skipped_deps;
    }
    if (is_runes() && untracked_writes !== null && !untracking && deps !== null && (reaction.f & (DERIVED | MAYBE_DIRTY | DIRTY)) === 0) {
      for (i = 0; i < /** @type {Source[]} */
      untracked_writes.length; i++) {
        schedule_possible_effect_self_invalidation(
          untracked_writes[i],
          /** @type {Effect} */
          reaction
        );
      }
    }
    if (previous_reaction !== null && previous_reaction !== reaction) {
      read_version++;
      if (previous_reaction.deps !== null) {
        for (let i2 = 0; i2 < previous_skipped_deps; i2 += 1) {
          previous_reaction.deps[i2].rv = read_version;
        }
      }
      if (previous_deps !== null) {
        for (const dep of previous_deps) {
          dep.rv = read_version;
        }
      }
      if (untracked_writes !== null) {
        if (previous_untracked_writes === null) {
          previous_untracked_writes = untracked_writes;
        } else {
          previous_untracked_writes.push(.../** @type {Source[]} */
          untracked_writes);
        }
      }
    }
    if ((reaction.f & ERROR_VALUE) !== 0) {
      reaction.f ^= ERROR_VALUE;
    }
    return result;
  } catch (error) {
    return handle_error(error);
  } finally {
    reaction.f ^= REACTION_IS_UPDATING;
    new_deps = previous_deps;
    skipped_deps = previous_skipped_deps;
    untracked_writes = previous_untracked_writes;
    active_reaction = previous_reaction;
    current_sources = previous_sources;
    set_component_context(previous_component_context);
    untracking = previous_untracking;
    update_version = previous_update_version;
  }
}
function remove_reaction(signal, dependency) {
  let reactions = dependency.reactions;
  if (reactions !== null) {
    var index2 = index_of.call(reactions, signal);
    if (index2 !== -1) {
      var new_length = reactions.length - 1;
      if (new_length === 0) {
        reactions = dependency.reactions = null;
      } else {
        reactions[index2] = reactions[new_length];
        reactions.pop();
      }
    }
  }
  if (reactions === null && (dependency.f & DERIVED) !== 0 && // Destroying a child effect while updating a parent effect can cause a dependency to appear
  // to be unused, when in fact it is used by the currently-updating parent. Checking `new_deps`
  // allows us to skip the expensive work of disconnecting and immediately reconnecting it
  (new_deps === null || !includes.call(new_deps, dependency))) {
    var derived3 = (
      /** @type {Derived} */
      dependency
    );
    if ((derived3.f & CONNECTED) !== 0) {
      derived3.f ^= CONNECTED;
      derived3.f &= ~WAS_MARKED;
    }
    if (derived3.v !== UNINITIALIZED) {
      update_derived_status(derived3);
    }
    freeze_derived_effects(derived3);
    remove_reactions(derived3, 0);
  }
}
function remove_reactions(signal, start_index) {
  var dependencies = signal.deps;
  if (dependencies === null) return;
  for (var i = start_index; i < dependencies.length; i++) {
    remove_reaction(signal, dependencies[i]);
  }
}
function update_effect(effect2) {
  var flags2 = effect2.f;
  if ((flags2 & DESTROYED) !== 0) {
    return;
  }
  set_signal_status(effect2, CLEAN);
  var previous_effect = active_effect;
  var was_updating_effect = is_updating_effect;
  active_effect = effect2;
  is_updating_effect = true;
  if (dev_fallback_default) {
    var previous_component_fn = dev_current_component_function;
    set_dev_current_component_function(effect2.component_function);
    var previous_stack = (
      /** @type {any} */
      dev_stack
    );
    set_dev_stack(effect2.dev_stack ?? dev_stack);
  }
  try {
    if ((flags2 & (BLOCK_EFFECT | MANAGED_EFFECT)) !== 0) {
      destroy_block_effect_children(effect2);
    } else {
      destroy_effect_children(effect2);
    }
    execute_effect_teardown(effect2);
    var teardown2 = update_reaction(effect2);
    effect2.teardown = typeof teardown2 === "function" ? teardown2 : null;
    effect2.wv = write_version;
    if (dev_fallback_default && tracing_mode_flag && (effect2.f & DIRTY) !== 0 && effect2.deps !== null) {
      for (var dep of effect2.deps) {
        if (dep.set_during_effect) {
          dep.wv = increment_write_version();
          dep.set_during_effect = false;
        }
      }
    }
  } finally {
    is_updating_effect = was_updating_effect;
    active_effect = previous_effect;
    if (dev_fallback_default) {
      set_dev_current_component_function(previous_component_fn);
      set_dev_stack(previous_stack);
    }
  }
}
async function tick() {
  if (async_mode_flag) {
    return new Promise((f) => {
      requestAnimationFrame(() => f());
      setTimeout(() => f());
    });
  }
  await Promise.resolve();
  flushSync();
}
function get2(signal) {
  var flags2 = signal.f;
  var is_derived = (flags2 & DERIVED) !== 0;
  captured_signals?.add(signal);
  if (active_reaction !== null && !untracking) {
    var destroyed = active_effect !== null && (active_effect.f & DESTROYED) !== 0;
    if (!destroyed && (current_sources === null || !current_sources.has(signal))) {
      var deps = active_reaction.deps;
      if ((active_reaction.f & REACTION_IS_UPDATING) !== 0) {
        if (signal.rv < read_version) {
          signal.rv = read_version;
          if (new_deps === null && deps !== null && deps[skipped_deps] === signal) {
            skipped_deps++;
          } else if (new_deps === null) {
            new_deps = [signal];
          } else {
            new_deps.push(signal);
          }
        }
      } else {
        active_reaction.deps ??= [];
        if (!includes.call(active_reaction.deps, signal)) {
          active_reaction.deps.push(signal);
        }
        var reactions = signal.reactions;
        if (reactions === null) {
          signal.reactions = [active_reaction];
        } else if (!includes.call(reactions, active_reaction)) {
          reactions.push(active_reaction);
        }
      }
    }
  }
  if (dev_fallback_default) {
    if (!untracking && reactivity_loss_tracker && !reactivity_loss_tracker.warned && (reactivity_loss_tracker.effect.f & REACTION_IS_UPDATING) === 0 && !reactivity_loss_tracker.effect_deps.has(signal)) {
      reactivity_loss_tracker.warned = true;
      await_reactivity_loss(
        /** @type {string} */
        signal.label
      );
      var trace2 = get_error("traced at");
      if (trace2) console.warn(trace2);
    }
    recent_async_deriveds.delete(signal);
    if (tracing_mode_flag && !untracking && tracing_expressions !== null && active_reaction !== null && tracing_expressions.reaction === active_reaction) {
      if (signal.trace) {
        signal.trace();
      } else {
        trace2 = get_error("traced at");
        if (trace2) {
          var entry = tracing_expressions.entries.get(signal);
          if (entry === void 0) {
            entry = { traces: [] };
            tracing_expressions.entries.set(signal, entry);
          }
          var last = entry.traces[entry.traces.length - 1];
          if (trace2.stack !== last?.stack) {
            entry.traces.push(trace2);
          }
        }
      }
    }
  }
  if (is_destroying_effect && old_values.has(signal)) {
    return old_values.get(signal);
  }
  if (is_derived) {
    var derived3 = (
      /** @type {Derived} */
      signal
    );
    if (is_destroying_effect) {
      var value = derived3.v;
      if ((derived3.f & CLEAN) === 0 && derived3.reactions !== null || depends_on_old_values(derived3)) {
        value = execute_derived(derived3);
      }
      old_values.set(derived3, value);
      return value;
    }
    var should_connect = (derived3.f & CONNECTED) === 0 && !untracking && active_reaction !== null && (is_updating_effect || (active_reaction.f & CONNECTED) !== 0);
    var is_new = (derived3.f & REACTION_RAN) === 0;
    if (is_dirty(derived3)) {
      if (should_connect) {
        derived3.f |= CONNECTED;
      }
      update_derived(derived3);
    }
    if (should_connect && !is_new) {
      unfreeze_derived_effects(derived3);
      reconnect(derived3);
    }
  }
  if (batch_values?.has(signal)) {
    return batch_values.get(signal);
  }
  if ((signal.f & ERROR_VALUE) !== 0) {
    throw signal.v;
  }
  return signal.v;
}
function reconnect(derived3) {
  derived3.f |= CONNECTED;
  if (derived3.deps === null) return;
  for (const dep of derived3.deps) {
    (dep.reactions ??= []).push(derived3);
    if ((dep.f & DERIVED) !== 0 && (dep.f & CONNECTED) === 0) {
      unfreeze_derived_effects(
        /** @type {Derived} */
        dep
      );
      reconnect(
        /** @type {Derived} */
        dep
      );
    }
  }
}
function depends_on_old_values(derived3) {
  if (derived3.v === UNINITIALIZED) return true;
  if (derived3.deps === null) return false;
  for (const dep of derived3.deps) {
    if (old_values.has(dep)) {
      return true;
    }
    if ((dep.f & DERIVED) !== 0 && depends_on_old_values(
      /** @type {Derived} */
      dep
    )) {
      return true;
    }
  }
  return false;
}
function untrack(fn) {
  var previous_untracking = untracking;
  try {
    untracking = true;
    return fn();
  } finally {
    untracking = previous_untracking;
  }
}

// ../../../node_modules/svelte/src/utils.js
var DOM_BOOLEAN_ATTRIBUTES = [
  "allowfullscreen",
  "async",
  "autofocus",
  "autoplay",
  "checked",
  "controls",
  "default",
  "disabled",
  "formnovalidate",
  "indeterminate",
  "inert",
  "ismap",
  "loop",
  "multiple",
  "muted",
  "nomodule",
  "novalidate",
  "open",
  "playsinline",
  "readonly",
  "required",
  "reversed",
  "seamless",
  "selected",
  "webkitdirectory",
  "defer",
  "disablepictureinpicture",
  "disableremoteplayback"
];
var DOM_PROPERTIES = [
  ...DOM_BOOLEAN_ATTRIBUTES,
  "formNoValidate",
  "isMap",
  "noModule",
  "playsInline",
  "readOnly",
  "value",
  "volume",
  "defaultValue",
  "defaultChecked",
  "srcObject",
  "noValidate",
  "allowFullscreen",
  "disablePictureInPicture",
  "disableRemotePlayback"
];
var PASSIVE_EVENTS = ["touchstart", "touchmove"];
function is_passive_event(name) {
  return PASSIVE_EVENTS.includes(name);
}
var STATE_CREATION_RUNES = (
  /** @type {const} */
  [
    "$state",
    "$state.raw",
    "$derived",
    "$derived.by"
  ]
);
var RUNES = (
  /** @type {const} */
  [
    ...STATE_CREATION_RUNES,
    "$state.eager",
    "$state.snapshot",
    "$props",
    "$props.id",
    "$bindable",
    "$effect",
    "$effect.pre",
    "$effect.tracking",
    "$effect.root",
    "$effect.pending",
    "$inspect",
    "$inspect().with",
    "$inspect.trace",
    "$host"
  ]
);

// ../../../node_modules/svelte/src/internal/client/dev/css.js
var all_styles = /* @__PURE__ */ new Map();
function register_style(hash2, style) {
  var styles = all_styles.get(hash2);
  if (!styles) {
    styles = /* @__PURE__ */ new Set();
    all_styles.set(hash2, styles);
  }
  styles.add(style);
}

// ../../../node_modules/svelte/src/internal/client/dom/elements/events.js
var event_symbol = /* @__PURE__ */ Symbol("events");
var all_registered_events = /* @__PURE__ */ new Set();
var root_event_handles = /* @__PURE__ */ new Set();
function create_event(event_name, dom, handler, options = {}) {
  function target_handler(event2) {
    if (!options.capture) {
      handle_event_propagation.call(dom, event2);
    }
    if (!event2.cancelBubble) {
      return without_reactive_context(() => {
        return handler?.call(this, event2);
      });
    }
  }
  if (event_name.startsWith("pointer") || event_name.startsWith("touch") || event_name === "wheel") {
    queue_micro_task(() => {
      dom.addEventListener(event_name, target_handler, options);
    });
  } else {
    dom.addEventListener(event_name, target_handler, options);
  }
  return target_handler;
}
function event(event_name, dom, handler, capture2, passive2) {
  var options = { capture: capture2, passive: passive2 };
  var target_handler = create_event(event_name, dom, handler, options);
  if (dom === document.body || // @ts-ignore
  dom === window || // @ts-ignore
  dom === document || // Firefox has quirky behavior, it can happen that we still get "canplay" events when the element is already removed
  dom instanceof HTMLMediaElement) {
    teardown(() => {
      dom.removeEventListener(event_name, target_handler, options);
    });
  }
}
function delegated(event_name, element2, handler) {
  (element2[event_symbol] ??= {})[event_name] = handler;
}
function delegate(events) {
  for (var i = 0; i < events.length; i++) {
    all_registered_events.add(events[i]);
  }
  for (var fn of root_event_handles) {
    fn(events);
  }
}
var last_propagated_event = null;
function handle_event_propagation(event2) {
  var handler_element = this;
  var owner_document = (
    /** @type {Node} */
    handler_element.ownerDocument
  );
  var event_name = event2.type;
  var path = event2.composedPath?.() || [];
  var current_target = (
    /** @type {null | Element} */
    path[0] || event2.target
  );
  last_propagated_event = event2;
  var path_idx = 0;
  var handled_at = last_propagated_event === event2 && event2[event_symbol];
  if (handled_at) {
    var at_idx = path.indexOf(handled_at);
    if (at_idx !== -1 && (handler_element === document || handler_element === /** @type {any} */
    window)) {
      event2[event_symbol] = handler_element;
      return;
    }
    var handler_idx = path.indexOf(handler_element);
    if (handler_idx === -1) {
      return;
    }
    if (at_idx <= handler_idx) {
      path_idx = at_idx;
    }
  }
  current_target = /** @type {Element} */
  path[path_idx] || event2.target;
  if (current_target === handler_element) return;
  define_property(event2, "currentTarget", {
    configurable: true,
    get() {
      return current_target || owner_document;
    }
  });
  var previous_reaction = active_reaction;
  var previous_effect = active_effect;
  set_active_reaction(null);
  set_active_effect(null);
  try {
    var throw_error;
    var other_errors = [];
    while (current_target !== null) {
      if (current_target === handler_element) break;
      try {
        var delegated2 = current_target[event_symbol]?.[event_name];
        if (delegated2 != null && (!/** @type {any} */
        current_target.disabled || // DOM could've been updated already by the time this is reached, so we check this as well
        // -> the target could not have been disabled because it emits the event in the first place
        event2.target === current_target)) {
          delegated2.call(current_target, event2);
        }
      } catch (error) {
        if (throw_error) {
          other_errors.push(error);
        } else {
          throw_error = error;
        }
      }
      if (event2.cancelBubble) break;
      path_idx++;
      current_target = path_idx < path.length ? (
        /** @type {Element} */
        path[path_idx]
      ) : null;
    }
    if (throw_error) {
      for (let error of other_errors) {
        queueMicrotask(() => {
          throw error;
        });
      }
      throw throw_error;
    }
  } finally {
    event2[event_symbol] = handler_element;
    delete event2.currentTarget;
    set_active_reaction(previous_reaction);
    set_active_effect(previous_effect);
  }
}

// ../../../node_modules/svelte/src/internal/client/dom/reconciler.js
var policy = (
  // We gotta write it like this because after downleveling the pure comment may end up in the wrong location
  globalThis?.window?.trustedTypes && /* @__PURE__ */ globalThis.window.trustedTypes.createPolicy("svelte-trusted-html", {
    /** @param {string} html */
    createHTML: (html2) => {
      return html2;
    }
  })
);
function create_trusted_html(html2) {
  return (
    /** @type {string} */
    policy?.createHTML(html2) ?? html2
  );
}
function create_fragment_from_html(html2) {
  var elem = create_element("template");
  elem.innerHTML = create_trusted_html(html2.replaceAll("<!>", "<!---->"));
  return elem.content;
}

// ../../../node_modules/svelte/src/internal/client/dom/template.js
function assign_nodes(start, end) {
  var effect2 = (
    /** @type {Effect} */
    active_effect
  );
  if (effect2.nodes === null) {
    effect2.nodes = { start, end, a: null, t: null };
  }
}
// @__NO_SIDE_EFFECTS__
function from_html(content, flags2) {
  var is_fragment = (flags2 & TEMPLATE_FRAGMENT) !== 0;
  var use_import_node = (flags2 & TEMPLATE_USE_IMPORT_NODE) !== 0;
  var node;
  var has_start = !content.startsWith("<!>");
  return () => {
    if (hydrating) {
      assign_nodes(hydrate_node, null);
      return hydrate_node;
    }
    if (node === void 0) {
      node = create_fragment_from_html(has_start ? content : "<!>" + content);
      if (!is_fragment) node = /** @type {TemplateNode} */
      get_first_child(node);
    }
    var clone = (
      /** @type {TemplateNode} */
      use_import_node || is_firefox ? document.importNode(node, true) : node.cloneNode(true)
    );
    if (is_fragment) {
      var start = (
        /** @type {TemplateNode} */
        get_first_child(clone)
      );
      var end = (
        /** @type {TemplateNode} */
        clone.lastChild
      );
      assign_nodes(start, end);
    } else {
      assign_nodes(clone, clone);
    }
    return clone;
  };
}
function comment() {
  if (hydrating) {
    assign_nodes(hydrate_node, null);
    return hydrate_node;
  }
  var frag = document.createDocumentFragment();
  var start = document.createComment("");
  var anchor = create_text();
  frag.append(start, anchor);
  assign_nodes(start, anchor);
  return frag;
}
function append(anchor, dom) {
  if (hydrating) {
    var effect2 = (
      /** @type {Effect & { nodes: EffectNodes }} */
      active_effect
    );
    if ((effect2.f & REACTION_RAN) === 0 || effect2.nodes.end === null) {
      effect2.nodes.end = hydrate_node;
    }
    hydrate_next();
    return;
  }
  if (anchor === null) {
    return;
  }
  anchor.before(
    /** @type {Node} */
    dom
  );
}

// ../../../node_modules/svelte/src/internal/client/render.js
var should_intro = true;
function set_text(text2, value) {
  var str = value == null ? "" : typeof value === "object" ? `${value}` : value;
  if (str !== /** @type {any} */
  (text2[TEXT_CACHE] ??= text2.nodeValue)) {
    text2[TEXT_CACHE] = str;
    text2.nodeValue = `${str}`;
  }
}
function mount(component2, options) {
  return _mount(component2, options);
}
function hydrate(component2, options) {
  init_operations();
  options.intro = options.intro ?? false;
  const target = options.target;
  const was_hydrating = hydrating;
  const previous_hydrate_node = hydrate_node;
  try {
    var anchor = get_first_child(target);
    while (anchor && (anchor.nodeType !== COMMENT_NODE || /** @type {Comment} */
    anchor.data !== HYDRATION_START)) {
      anchor = get_next_sibling(anchor);
    }
    if (!anchor) {
      throw HYDRATION_ERROR;
    }
    set_hydrating(true);
    set_hydrate_node(
      /** @type {Comment} */
      anchor
    );
    const instance = _mount(component2, { ...options, anchor });
    set_hydrating(false);
    return (
      /**  @type {Exports} */
      instance
    );
  } catch (error) {
    if (error instanceof Error && error.message.split("\n").some((line) => line.startsWith("https://svelte.dev/e/"))) {
      throw error;
    }
    if (error !== HYDRATION_ERROR) {
      console.warn("Failed to hydrate: ", error);
    }
    if (options.recover === false) {
      hydration_failed();
    }
    init_operations();
    clear_text_content(target);
    set_hydrating(false);
    return mount(component2, options);
  } finally {
    set_hydrating(was_hydrating);
    set_hydrate_node(previous_hydrate_node);
  }
}
var listeners = /* @__PURE__ */ new Map();
function _mount(Component, { target, anchor, props = {}, events, context, intro = true, transformError }) {
  init_operations();
  var component2 = void 0;
  var unmount2 = component_root(() => {
    var anchor_node = anchor ?? target.appendChild(create_text());
    boundary(
      /** @type {TemplateNode} */
      anchor_node,
      {
        pending: () => {
        }
      },
      (anchor_node2) => {
        push({});
        var ctx = (
          /** @type {ComponentContext} */
          component_context
        );
        if (context) ctx.c = context;
        if (events) {
          props.$$events = events;
        }
        if (hydrating) {
          assign_nodes(
            /** @type {TemplateNode} */
            anchor_node2,
            null
          );
        }
        should_intro = intro;
        component2 = Component(anchor_node2, props) || {};
        should_intro = true;
        if (hydrating) {
          active_effect.nodes.end = hydrate_node;
          if (hydrate_node === null || hydrate_node.nodeType !== COMMENT_NODE || /** @type {Comment} */
          hydrate_node.data !== HYDRATION_END) {
            hydration_mismatch();
            throw HYDRATION_ERROR;
          }
        }
        pop();
      },
      transformError
    );
    var registered_events = /* @__PURE__ */ new Set();
    var event_handle = (events2) => {
      for (var i = 0; i < events2.length; i++) {
        var event_name = events2[i];
        if (registered_events.has(event_name)) continue;
        registered_events.add(event_name);
        var passive2 = is_passive_event(event_name);
        for (const node of [target, document]) {
          var counts = listeners.get(node);
          if (counts === void 0) {
            counts = /* @__PURE__ */ new Map();
            listeners.set(node, counts);
          }
          var count = counts.get(event_name);
          if (count === void 0) {
            node.addEventListener(event_name, handle_event_propagation, { passive: passive2 });
            counts.set(event_name, 1);
          } else {
            counts.set(event_name, count + 1);
          }
        }
      }
    };
    event_handle(array_from(all_registered_events));
    root_event_handles.add(event_handle);
    return () => {
      for (var event_name of registered_events) {
        for (const node of [target, document]) {
          var counts = (
            /** @type {Map<string, number>} */
            listeners.get(node)
          );
          var count = (
            /** @type {number} */
            counts.get(event_name)
          );
          if (--count == 0) {
            node.removeEventListener(event_name, handle_event_propagation);
            counts.delete(event_name);
            if (counts.size === 0) {
              listeners.delete(node);
            }
          } else {
            counts.set(event_name, count);
          }
        }
      }
      root_event_handles.delete(event_handle);
      if (anchor_node !== anchor) {
        anchor_node.parentNode?.removeChild(anchor_node);
      }
    };
  });
  mounted_components.set(component2, unmount2);
  return component2;
}
var mounted_components = /* @__PURE__ */ new WeakMap();
function unmount(component2, options) {
  const fn = mounted_components.get(component2);
  if (fn) {
    mounted_components.delete(component2);
    return fn(options);
  }
  if (dev_fallback_default) {
    if (STATE_SYMBOL in component2) {
      state_proxy_unmount();
    } else {
      lifecycle_double_unmount();
    }
  }
  return Promise.resolve();
}

// ../../../node_modules/svelte/src/internal/client/dom/blocks/branches.js
var BranchManager = class {
  /** @type {TemplateNode} */
  anchor;
  /** @type {Map<Batch, Key>} */
  #batches = /* @__PURE__ */ new Map();
  /**
   * Map of keys to effects that are currently rendered in the DOM.
   * These effects are visible and actively part of the document tree.
   * Example:
   * ```
   * {#if condition}
   * 	foo
   * {:else}
   * 	bar
   * {/if}
   * ```
   * Can result in the entries `true->Effect` and `false->Effect`
   * @type {Map<Key, Effect>}
   */
  #onscreen = /* @__PURE__ */ new Map();
  /**
   * Similar to #onscreen with respect to the keys, but contains branches that are not yet
   * in the DOM, because their insertion is deferred.
   * @type {Map<Key, Branch>}
   */
  #offscreen = /* @__PURE__ */ new Map();
  /**
   * Keys of effects that are currently outroing
   * @type {Set<Key>}
   */
  #outroing = /* @__PURE__ */ new Set();
  /**
   * Whether to pause (i.e. outro) on change, or destroy immediately.
   * This is necessary for `<svelte:element>`
   */
  #transition = true;
  /**
   * @param {TemplateNode} anchor
   * @param {boolean} transition
   */
  constructor(anchor, transition2 = true) {
    this.anchor = anchor;
    this.#transition = transition2;
  }
  /**
   * @param {Batch} batch
   */
  #commit = (batch) => {
    if (!this.#batches.has(batch)) return;
    var key2 = (
      /** @type {Key} */
      this.#batches.get(batch)
    );
    var onscreen = this.#onscreen.get(key2);
    if (onscreen) {
      resume_effect(onscreen);
      this.#outroing.delete(key2);
    } else {
      var offscreen = this.#offscreen.get(key2);
      if (offscreen) {
        resume_effect(offscreen.effect);
        this.#onscreen.set(key2, offscreen.effect);
        this.#offscreen.delete(key2);
        if (dev_fallback_default) {
          offscreen.fragment.lastChild[HMR_ANCHOR] = this.anchor;
        }
        offscreen.fragment.lastChild.remove();
        this.anchor.before(offscreen.fragment);
        onscreen = offscreen.effect;
      }
    }
    for (const [b, k] of this.#batches) {
      this.#batches.delete(b);
      if (b === batch) {
        break;
      }
      const offscreen2 = this.#offscreen.get(k);
      if (offscreen2) {
        destroy_effect(offscreen2.effect);
        this.#offscreen.delete(k);
      }
    }
    for (const [k, effect2] of this.#onscreen) {
      if (k === key2 || this.#outroing.has(k)) continue;
      const on_destroy = () => {
        const keys = Array.from(this.#batches.values());
        if (keys.includes(k)) {
          var fragment = document.createDocumentFragment();
          move_effect(effect2, fragment);
          fragment.append(create_text());
          this.#offscreen.set(k, { effect: effect2, fragment });
        } else {
          destroy_effect(effect2);
        }
        this.#outroing.delete(k);
        this.#onscreen.delete(k);
      };
      if (this.#transition || !onscreen) {
        this.#outroing.add(k);
        pause_effect(effect2, on_destroy, false);
      } else {
        on_destroy();
      }
    }
  };
  /**
   * @param {Batch} batch
   */
  #discard = (batch) => {
    this.#batches.delete(batch);
    const keys = Array.from(this.#batches.values());
    for (const [k, branch2] of this.#offscreen) {
      if (!keys.includes(k)) {
        destroy_effect(branch2.effect);
        this.#offscreen.delete(k);
      }
    }
  };
  /**
   *
   * @param {any} key
   * @param {null | ((target: TemplateNode) => void)} fn
   */
  ensure(key2, fn) {
    var batch = (
      /** @type {Batch} */
      current_batch
    );
    var defer = should_defer_append();
    if (fn && !this.#onscreen.has(key2) && !this.#offscreen.has(key2)) {
      if (defer) {
        var fragment = document.createDocumentFragment();
        var target = create_text();
        fragment.append(target);
        this.#offscreen.set(key2, {
          effect: branch(() => fn(target)),
          fragment
        });
      } else {
        this.#onscreen.set(
          key2,
          branch(() => fn(this.anchor))
        );
      }
    }
    this.#batches.set(batch, key2);
    if (defer) {
      for (const [k, effect2] of this.#onscreen) {
        if (k === key2) {
          batch.unskip_effect(effect2);
        } else {
          batch.skip_effect(effect2);
        }
      }
      for (const [k, branch2] of this.#offscreen) {
        if (k === key2) {
          batch.unskip_effect(branch2.effect);
        } else {
          batch.skip_effect(branch2.effect);
        }
      }
      batch.oncommit(this.#commit);
      batch.ondiscard(this.#discard);
    } else {
      if (hydrating) {
        this.anchor = hydrate_node;
      }
      this.#commit(batch);
    }
  }
};

// ../../../node_modules/svelte/src/internal/client/dom/blocks/if.js
function if_block(node, fn, elseif = false) {
  var marker;
  if (hydrating) {
    marker = hydrate_node;
    hydrate_next();
  }
  var branches = new BranchManager(node);
  var flags2 = elseif ? EFFECT_TRANSPARENT : 0;
  function update_branch(key2, fn2) {
    if (hydrating) {
      var data = read_hydration_instruction(
        /** @type {TemplateNode} */
        marker
      );
      if (key2 !== parseInt(data.substring(1))) {
        var anchor = skip_nodes();
        set_hydrate_node(anchor);
        branches.anchor = anchor;
        set_hydrating(false);
        branches.ensure(key2, fn2);
        set_hydrating(true);
        return;
      }
    }
    branches.ensure(key2, fn2);
  }
  block(() => {
    var has_branch = false;
    fn((fn2, key2 = 0) => {
      has_branch = true;
      update_branch(key2, fn2);
    });
    if (!has_branch) {
      update_branch(-1, null);
    }
  }, flags2);
}

// ../../../node_modules/svelte/src/internal/client/dom/blocks/each.js
function pause_effects(state3, to_destroy, controlled_anchor) {
  var transitions = [];
  var length = to_destroy.length;
  var group;
  var remaining = to_destroy.length;
  for (var i = 0; i < length; i++) {
    let effect2 = to_destroy[i];
    pause_effect(
      effect2,
      () => {
        if (group) {
          group.pending.delete(effect2);
          group.done.add(effect2);
          if (group.pending.size === 0) {
            var groups = (
              /** @type {Set<EachOutroGroup>} */
              state3.outrogroups
            );
            destroy_effects(state3, array_from(group.done));
            groups.delete(group);
            if (groups.size === 0) {
              state3.outrogroups = null;
            }
          }
        } else {
          remaining -= 1;
        }
      },
      false
    );
  }
  if (remaining === 0) {
    var fast_path = transitions.length === 0 && controlled_anchor !== null;
    if (fast_path) {
      var anchor = (
        /** @type {Element} */
        controlled_anchor
      );
      var parent_node = (
        /** @type {Element} */
        anchor.parentNode
      );
      clear_text_content(parent_node);
      parent_node.append(anchor);
      state3.items.clear();
    }
    destroy_effects(state3, to_destroy, !fast_path);
  } else {
    group = {
      pending: new Set(to_destroy),
      done: /* @__PURE__ */ new Set()
    };
    (state3.outrogroups ??= /* @__PURE__ */ new Set()).add(group);
  }
}
function destroy_effects(state3, to_destroy, remove_dom = true) {
  var preserved_effects;
  if (state3.pending.size > 0) {
    preserved_effects = /* @__PURE__ */ new Set();
    for (const keys of state3.pending.values()) {
      for (const key2 of keys) {
        preserved_effects.add(
          /** @type {EachItem} */
          state3.items.get(key2).e
        );
      }
    }
  }
  for (var i = 0; i < to_destroy.length; i++) {
    var e = to_destroy[i];
    if (preserved_effects?.has(e)) {
      e.f |= EFFECT_OFFSCREEN;
      const fragment = document.createDocumentFragment();
      move_effect(e, fragment);
    } else {
      destroy_effect(to_destroy[i], remove_dom);
    }
  }
}
var offscreen_anchor;
function each(node, flags2, get_collection, get_key, render_fn, fallback_fn = null) {
  var anchor = node;
  var items = /* @__PURE__ */ new Map();
  var is_controlled = (flags2 & EACH_IS_CONTROLLED) !== 0;
  if (is_controlled) {
    var parent_node = (
      /** @type {Element} */
      node
    );
    anchor = hydrating ? set_hydrate_node(get_first_child(parent_node)) : parent_node.appendChild(create_text());
  }
  if (hydrating) {
    hydrate_next();
  }
  var fallback2 = null;
  var each_array = derived_safe_equal(() => {
    var collection = get_collection();
    return (
      /** @type {V[]} */
      is_array(collection) ? collection : collection == null ? [] : array_from(collection)
    );
  });
  if (dev_fallback_default) {
    tag(each_array, "{#each ...}");
  }
  var array;
  var pending2 = /* @__PURE__ */ new Map();
  var first_run = true;
  function commit(batch) {
    if ((state3.effect.f & DESTROYED) !== 0) {
      return;
    }
    state3.pending.delete(batch);
    state3.fallback = fallback2;
    reconcile(state3, array, anchor, flags2, get_key);
    if (fallback2 !== null) {
      if (array.length === 0) {
        if ((fallback2.f & EFFECT_OFFSCREEN) === 0) {
          resume_effect(fallback2);
        } else {
          fallback2.f ^= EFFECT_OFFSCREEN;
          move(fallback2, null, anchor);
        }
      } else {
        pause_effect(fallback2, () => {
          fallback2 = null;
        });
      }
    }
  }
  function discard(batch) {
    state3.pending.delete(batch);
  }
  var effect2 = block(() => {
    array = /** @type {V[]} */
    get2(each_array);
    var length = array.length;
    let mismatch = false;
    if (hydrating) {
      var is_else = read_hydration_instruction(anchor) === HYDRATION_START_ELSE;
      if (is_else !== (length === 0)) {
        anchor = skip_nodes();
        set_hydrate_node(anchor);
        set_hydrating(false);
        mismatch = true;
      }
    }
    var keys = /* @__PURE__ */ new Set();
    var batch = (
      /** @type {Batch} */
      current_batch
    );
    var defer = should_defer_append();
    for (var index2 = 0; index2 < length; index2 += 1) {
      if (hydrating && hydrate_node.nodeType === COMMENT_NODE && /** @type {Comment} */
      hydrate_node.data === HYDRATION_END) {
        anchor = /** @type {Comment} */
        hydrate_node;
        mismatch = true;
        set_hydrating(false);
      }
      var value = array[index2];
      var key2 = get_key(value, index2);
      if (dev_fallback_default) {
        var key_again = get_key(value, index2);
        if (key2 !== key_again) {
          each_key_volatile(String(index2), String(key2), String(key_again));
        }
      }
      var item = first_run ? null : items.get(key2);
      if (item) {
        if (item.v) internal_set(item.v, value);
        if (item.i) internal_set(item.i, index2);
        if (defer) {
          batch.unskip_effect(item.e);
        }
      } else {
        item = create_item(
          items,
          first_run ? anchor : offscreen_anchor ??= create_text(),
          value,
          key2,
          index2,
          render_fn,
          flags2,
          get_collection
        );
        if (!first_run) {
          item.e.f |= EFFECT_OFFSCREEN;
        }
        items.set(key2, item);
      }
      keys.add(key2);
    }
    if (length === 0 && fallback_fn && !fallback2) {
      if (first_run) {
        fallback2 = branch(() => fallback_fn(anchor));
      } else {
        fallback2 = branch(() => fallback_fn(offscreen_anchor ??= create_text()));
        fallback2.f |= EFFECT_OFFSCREEN;
      }
    }
    if (length > keys.size) {
      if (dev_fallback_default) {
        validate_each_keys(array, get_key);
      } else {
        each_key_duplicate("", "", "");
      }
    }
    if (hydrating && length > 0) {
      set_hydrate_node(skip_nodes());
    }
    if (!first_run) {
      pending2.set(batch, keys);
      if (defer) {
        for (const [key3, item2] of items) {
          if (!keys.has(key3)) {
            batch.skip_effect(item2.e);
          }
        }
        batch.oncommit(commit);
        batch.ondiscard(discard);
      } else {
        commit(batch);
      }
    }
    if (mismatch) {
      set_hydrating(true);
    }
    get2(each_array);
  });
  var state3 = { effect: effect2, flags: flags2, items, pending: pending2, outrogroups: null, fallback: fallback2 };
  first_run = false;
  if (hydrating) {
    anchor = hydrate_node;
  }
}
function skip_to_branch(effect2) {
  while (effect2 !== null && (effect2.f & BRANCH_EFFECT) === 0) {
    effect2 = effect2.next;
  }
  return effect2;
}
function reconcile(state3, array, anchor, flags2, get_key) {
  var is_animated = (flags2 & EACH_IS_ANIMATED) !== 0;
  var length = array.length;
  var items = state3.items;
  var current = skip_to_branch(state3.effect.first);
  var seen;
  var prev = null;
  var to_animate;
  var matched = [];
  var stashed = [];
  var value;
  var key2;
  var effect2;
  var i;
  if (is_animated) {
    for (i = 0; i < length; i += 1) {
      value = array[i];
      key2 = get_key(value, i);
      effect2 = /** @type {EachItem} */
      items.get(key2).e;
      if ((effect2.f & EFFECT_OFFSCREEN) === 0) {
        effect2.nodes?.a?.measure();
        (to_animate ??= /* @__PURE__ */ new Set()).add(effect2);
      }
    }
  }
  for (i = 0; i < length; i += 1) {
    value = array[i];
    key2 = get_key(value, i);
    effect2 = /** @type {EachItem} */
    items.get(key2).e;
    if (state3.outrogroups !== null) {
      for (const group of state3.outrogroups) {
        group.pending.delete(effect2);
        group.done.delete(effect2);
      }
    }
    if ((effect2.f & INERT) !== 0) {
      resume_effect(effect2);
      if (is_animated) {
        effect2.nodes?.a?.unfix();
        (to_animate ??= /* @__PURE__ */ new Set()).delete(effect2);
      }
    }
    if ((effect2.f & EFFECT_OFFSCREEN) !== 0) {
      effect2.f ^= EFFECT_OFFSCREEN;
      if (effect2 === current) {
        move(effect2, null, anchor);
      } else {
        var next2 = prev ? prev.next : current;
        if (effect2 === state3.effect.last) {
          state3.effect.last = effect2.prev;
        }
        if (effect2.prev) effect2.prev.next = effect2.next;
        if (effect2.next) effect2.next.prev = effect2.prev;
        link(state3, prev, effect2);
        link(state3, effect2, next2);
        move(effect2, next2, anchor);
        prev = effect2;
        matched = [];
        stashed = [];
        current = skip_to_branch(prev.next);
        continue;
      }
    }
    if (effect2 !== current) {
      if (seen !== void 0 && seen.has(effect2)) {
        if (matched.length < stashed.length) {
          var start = stashed[0];
          var j;
          prev = start.prev;
          var a = matched[0];
          var b = matched[matched.length - 1];
          for (j = 0; j < matched.length; j += 1) {
            move(matched[j], start, anchor);
          }
          for (j = 0; j < stashed.length; j += 1) {
            seen.delete(stashed[j]);
          }
          link(state3, a.prev, b.next);
          link(state3, prev, a);
          link(state3, b, start);
          current = start;
          prev = b;
          i -= 1;
          matched = [];
          stashed = [];
        } else {
          seen.delete(effect2);
          move(effect2, current, anchor);
          link(state3, effect2.prev, effect2.next);
          link(state3, effect2, prev === null ? state3.effect.first : prev.next);
          link(state3, prev, effect2);
          prev = effect2;
        }
        continue;
      }
      matched = [];
      stashed = [];
      while (current !== null && current !== effect2) {
        (seen ??= /* @__PURE__ */ new Set()).add(current);
        stashed.push(current);
        current = skip_to_branch(current.next);
      }
      if (current === null) {
        continue;
      }
    }
    if ((effect2.f & EFFECT_OFFSCREEN) === 0) {
      matched.push(effect2);
    }
    prev = effect2;
    current = skip_to_branch(effect2.next);
  }
  if (state3.outrogroups !== null) {
    for (const group of state3.outrogroups) {
      if (group.pending.size === 0) {
        destroy_effects(state3, array_from(group.done));
        state3.outrogroups?.delete(group);
      }
    }
    if (state3.outrogroups.size === 0) {
      state3.outrogroups = null;
    }
  }
  if (current !== null || seen !== void 0) {
    var to_destroy = [];
    if (seen !== void 0) {
      for (effect2 of seen) {
        if ((effect2.f & INERT) === 0) {
          to_destroy.push(effect2);
        }
      }
    }
    while (current !== null) {
      if ((current.f & INERT) === 0 && current !== state3.fallback) {
        to_destroy.push(current);
      }
      current = skip_to_branch(current.next);
    }
    var destroy_length = to_destroy.length;
    if (destroy_length > 0) {
      var controlled_anchor = (flags2 & EACH_IS_CONTROLLED) !== 0 && length === 0 ? anchor : null;
      if (is_animated) {
        for (i = 0; i < destroy_length; i += 1) {
          to_destroy[i].nodes?.a?.measure();
        }
        for (i = 0; i < destroy_length; i += 1) {
          to_destroy[i].nodes?.a?.fix();
        }
      }
      pause_effects(state3, to_destroy, controlled_anchor);
    }
  }
  if (is_animated) {
    queue_micro_task(() => {
      if (to_animate === void 0) return;
      for (effect2 of to_animate) {
        effect2.nodes?.a?.apply();
      }
    });
  }
}
function create_item(items, anchor, value, key2, index2, render_fn, flags2, get_collection) {
  var v = (flags2 & EACH_ITEM_REACTIVE) !== 0 ? (flags2 & EACH_ITEM_IMMUTABLE) === 0 ? mutable_source(value, false, false) : source(value) : null;
  var i = (flags2 & EACH_INDEX_REACTIVE) !== 0 ? source(index2) : null;
  if (dev_fallback_default && v) {
    v.trace = () => {
      get_collection()[i?.v ?? index2];
    };
  }
  return {
    v,
    i,
    e: branch(() => {
      render_fn(anchor, v ?? value, i ?? index2, get_collection);
      return () => {
        items.delete(key2);
      };
    })
  };
}
function move(effect2, next2, anchor) {
  if (!effect2.nodes) return;
  var node = effect2.nodes.start;
  var end = effect2.nodes.end;
  var dest = next2 && (next2.f & EFFECT_OFFSCREEN) === 0 ? (
    /** @type {EffectNodes} */
    next2.nodes.start
  ) : anchor;
  while (node !== null) {
    var next_node = (
      /** @type {TemplateNode} */
      get_next_sibling(node)
    );
    dest.before(node);
    if (node === end) {
      return;
    }
    node = next_node;
  }
}
function link(state3, prev, next2) {
  if (prev === null) {
    state3.effect.first = next2;
  } else {
    prev.next = next2;
  }
  if (next2 === null) {
    state3.effect.last = prev;
  } else {
    next2.prev = prev;
  }
}
function validate_each_keys(array, key_fn) {
  const keys = /* @__PURE__ */ new Map();
  const length = array.length;
  for (let i = 0; i < length; i++) {
    const key2 = key_fn(array[i], i);
    if (keys.has(key2)) {
      const a = String(keys.get(key2));
      const b = String(i);
      let k = String(key2);
      if (k.startsWith("[object ")) k = null;
      each_key_duplicate(a, b, k);
    }
    keys.set(key2, i);
  }
}

// ../../../node_modules/svelte/src/internal/client/dom/blocks/svelte-component.js
function component(node, get_component, render_fn) {
  var hydration_start_node;
  if (hydrating) {
    hydration_start_node = hydrate_node;
    hydrate_next();
  }
  var branches = new BranchManager(node);
  block(() => {
    var component2 = get_component() ?? null;
    if (hydrating) {
      var data = read_hydration_instruction(
        /** @type {TemplateNode} */
        hydration_start_node
      );
      var server_had_component = data === HYDRATION_START;
      var client_has_component = component2 !== null;
      if (server_had_component !== client_has_component) {
        var anchor = skip_nodes();
        set_hydrate_node(anchor);
        branches.anchor = anchor;
        set_hydrating(false);
        branches.ensure(component2, component2 && ((target) => render_fn(target, component2)));
        set_hydrating(true);
        return;
      }
    }
    branches.ensure(component2, component2 && ((target) => render_fn(target, component2)));
  }, EFFECT_TRANSPARENT);
}

// ../../../node_modules/svelte/src/internal/client/dom/css.js
function append_styles(anchor, css) {
  effect(() => {
    var root15 = anchor.getRootNode();
    var target = (
      /** @type {ShadowRoot} */
      root15.host ? (
        /** @type {ShadowRoot} */
        root15
      ) : (
        /** @type {Document} */
        root15.head ?? /** @type {Document} */
        root15.ownerDocument.head
      )
    );
    if (!target.querySelector("#" + css.hash)) {
      const style = create_element("style");
      style.id = css.hash;
      style.textContent = css.code;
      target.appendChild(style);
      if (dev_fallback_default) {
        register_style(css.hash, style);
      }
    }
  });
}

// ../../../node_modules/svelte/src/internal/shared/attributes.js
var whitespace = [..." 	\n\r\f\xA0\v\uFEFF"];
function to_class(value, hash2, directives) {
  var classname = value == null ? "" : "" + value;
  if (hash2) {
    classname = classname ? classname + " " + hash2 : hash2;
  }
  if (directives) {
    for (var key2 of Object.keys(directives)) {
      if (directives[key2]) {
        classname = classname ? classname + " " + key2 : key2;
      } else if (classname.length) {
        var len = key2.length;
        var a = 0;
        while ((a = classname.indexOf(key2, a)) >= 0) {
          var b = a + len;
          if ((a === 0 || whitespace.includes(classname[a - 1])) && (b === classname.length || whitespace.includes(classname[b]))) {
            classname = (a === 0 ? "" : classname.substring(0, a)) + classname.substring(b + 1);
          } else {
            a = b;
          }
        }
      }
    }
  }
  return classname === "" ? null : classname;
}
function append_styles2(styles, important = false) {
  var separator = important ? " !important;" : ";";
  var css = "";
  for (var key2 of Object.keys(styles)) {
    var value = styles[key2];
    if (value != null && value !== "") {
      css += " " + key2 + ": " + value + separator;
    }
  }
  return css;
}
function to_css_name(name) {
  if (name[0] !== "-" || name[1] !== "-") {
    return name.toLowerCase();
  }
  return name;
}
function to_style(value, styles) {
  if (styles) {
    var new_style = "";
    var normal_styles;
    var important_styles;
    if (Array.isArray(styles)) {
      normal_styles = styles[0];
      important_styles = styles[1];
    } else {
      normal_styles = styles;
    }
    if (value) {
      value = String(value).replaceAll(/\s*\/\*.*?\*\/\s*/g, "").trim();
      var in_str = false;
      var in_apo = 0;
      var in_comment = false;
      var reserved_names = [];
      if (normal_styles) {
        reserved_names.push(...Object.keys(normal_styles).map(to_css_name));
      }
      if (important_styles) {
        reserved_names.push(...Object.keys(important_styles).map(to_css_name));
      }
      var start_index = 0;
      var name_index = -1;
      const len = value.length;
      for (var i = 0; i < len; i++) {
        var c = value[i];
        if (in_comment) {
          if (c === "/" && value[i - 1] === "*") {
            in_comment = false;
          }
        } else if (in_str) {
          if (in_str === c) {
            in_str = false;
          }
        } else if (c === "/" && value[i + 1] === "*") {
          in_comment = true;
        } else if (c === '"' || c === "'") {
          in_str = c;
        } else if (c === "(") {
          in_apo++;
        } else if (c === ")") {
          in_apo--;
        }
        if (!in_comment && in_str === false && in_apo === 0) {
          if (c === ":" && name_index === -1) {
            name_index = i;
          } else if (c === ";" || i === len - 1) {
            if (name_index !== -1) {
              var name = to_css_name(value.substring(start_index, name_index).trim());
              if (!reserved_names.includes(name)) {
                if (c !== ";") {
                  i++;
                }
                var property = value.substring(start_index, i).trim();
                new_style += " " + property + ";";
              }
            }
            start_index = i + 1;
            name_index = -1;
          }
        }
      }
    }
    if (normal_styles) {
      new_style += append_styles2(normal_styles);
    }
    if (important_styles) {
      new_style += append_styles2(important_styles, true);
    }
    new_style = new_style.trim();
    return new_style === "" ? null : new_style;
  }
  return value == null ? null : String(value);
}

// ../../../node_modules/svelte/src/internal/client/dom/elements/class.js
function set_class(dom, is_html, value, hash2, prev_classes, next_classes) {
  var prev = (
    /** @type {any} */
    dom[CLASS_CACHE]
  );
  if (hydrating || prev !== value || prev === void 0) {
    var next_class_name = to_class(value, hash2, next_classes);
    if (!hydrating || next_class_name !== dom.getAttribute("class")) {
      if (next_class_name == null) {
        dom.removeAttribute("class");
      } else if (is_html) {
        dom.className = next_class_name;
      } else {
        dom.setAttribute("class", next_class_name);
      }
    }
    dom[CLASS_CACHE] = value;
  } else if (next_classes && prev_classes !== next_classes) {
    for (var key2 in next_classes) {
      var is_present = !!next_classes[key2];
      if (prev_classes == null || is_present !== !!prev_classes[key2]) {
        dom.classList.toggle(key2, is_present);
      }
    }
  }
  return next_classes;
}

// ../../../node_modules/svelte/src/internal/client/dom/elements/style.js
function update_styles(dom, prev = {}, next2, priority) {
  for (var key2 in next2) {
    var value = next2[key2];
    if (prev[key2] !== value) {
      if (next2[key2] == null) {
        dom.style.removeProperty(key2);
      } else {
        dom.style.setProperty(key2, value, priority);
      }
    }
  }
}
function set_style(dom, value, prev_styles, next_styles) {
  var prev = (
    /** @type {any} */
    dom[STYLE_CACHE]
  );
  if (hydrating || prev !== value) {
    var next_style_attr = to_style(value, next_styles);
    if (!hydrating || next_style_attr !== dom.getAttribute("style")) {
      if (next_style_attr == null) {
        dom.removeAttribute("style");
      } else {
        dom.style.cssText = next_style_attr;
      }
    }
    dom[STYLE_CACHE] = value;
  } else if (next_styles) {
    if (Array.isArray(next_styles)) {
      update_styles(dom, prev_styles?.[0], next_styles[0]);
      update_styles(dom, prev_styles?.[1], next_styles[1], "important");
    } else {
      update_styles(dom, prev_styles, next_styles);
    }
  }
  return next_styles;
}

// ../../../node_modules/svelte/src/internal/client/dom/elements/attributes.js
var IS_CUSTOM_ELEMENT = /* @__PURE__ */ Symbol("is custom element");
var IS_HTML = /* @__PURE__ */ Symbol("is html");
var LINK_TAG = IS_XHTML ? "link" : "LINK";
var PROGRESS_TAG = IS_XHTML ? "progress" : "PROGRESS";
function remove_input_defaults(input) {
  if (!hydrating) return;
  var already_removed = false;
  var remove_defaults = () => {
    if (already_removed) return;
    already_removed = true;
    if (input.hasAttribute("value")) {
      var value = input.value;
      set_attribute2(input, "value", null);
      input.value = value;
    }
    if (input.hasAttribute("checked")) {
      var checked = input.checked;
      set_attribute2(input, "checked", null);
      input.checked = checked;
    }
  };
  input[FORM_RESET_HANDLER] = remove_defaults;
  queue_micro_task(remove_defaults);
  add_form_reset_listener();
}
function set_value(element2, value) {
  var attributes = get_attributes(element2);
  if (attributes.value === (attributes.value = // treat null and undefined the same for the initial value
  value ?? void 0) || // @ts-expect-error
  // `progress` elements always need their value set when it's `0`
  element2.value === value && (value !== 0 || element2.nodeName !== PROGRESS_TAG)) {
    return;
  }
  element2.value = value ?? "";
}
function set_attribute2(element2, attribute, value, skip_warning) {
  var attributes = get_attributes(element2);
  if (hydrating) {
    attributes[attribute] = element2.getAttribute(attribute);
    if (attribute === "src" || attribute === "srcset" || attribute === "href" && element2.nodeName === LINK_TAG) {
      if (!skip_warning) {
        check_src_in_dev_hydration(element2, attribute, value ?? "");
      }
      return;
    }
  }
  if (attributes[attribute] === (attributes[attribute] = value)) return;
  if (attribute === "loading") {
    element2[LOADING_ATTR_SYMBOL] = value;
  }
  if (value == null) {
    element2.removeAttribute(attribute);
  } else if (typeof value !== "string" && get_setters(element2).includes(attribute)) {
    element2[attribute] = value;
  } else {
    element2.setAttribute(attribute, value);
  }
}
function get_attributes(element2) {
  return (
    /** @type {Record<string | symbol, unknown>} **/
    /** @type {any} */
    element2[ATTRIBUTES_CACHE] ??= {
      [IS_CUSTOM_ELEMENT]: element2.nodeName.includes("-"),
      [IS_HTML]: element2.namespaceURI === NAMESPACE_HTML
    }
  );
}
var setters_cache = /* @__PURE__ */ new Map();
function get_setters(element2) {
  var cache_key = element2.getAttribute("is") || element2.nodeName;
  var setters = setters_cache.get(cache_key);
  if (setters) return setters;
  setters_cache.set(cache_key, setters = []);
  var descriptors;
  var proto = element2;
  var element_proto = Element.prototype;
  while (element_proto !== proto) {
    descriptors = get_descriptors(proto);
    for (var key2 in descriptors) {
      if (descriptors[key2].set && // better safe than sorry, we don't want spread attributes to mess with HTML content
      key2 !== "innerHTML" && key2 !== "textContent" && key2 !== "innerText") {
        setters.push(key2);
      }
    }
    proto = get_prototype_of(proto);
  }
  return setters;
}
function check_src_in_dev_hydration(element2, attribute, value) {
  if (!dev_fallback_default) return;
  if (attribute === "srcset" && srcset_url_equal(element2, value)) return;
  if (src_url_equal(element2.getAttribute(attribute) ?? "", value)) return;
  hydration_attribute_changed(
    attribute,
    element2.outerHTML.replace(element2.innerHTML, element2.innerHTML && "..."),
    String(value)
  );
}
function src_url_equal(element_src, url) {
  if (element_src === url) return true;
  return new URL(element_src, document.baseURI).href === new URL(url, document.baseURI).href;
}
function split_srcset(srcset) {
  return srcset.split(",").map((src) => src.trim().split(" ").filter(Boolean));
}
function srcset_url_equal(element2, srcset) {
  var element_urls = split_srcset(element2.srcset);
  var urls = split_srcset(srcset);
  return urls.length === element_urls.length && urls.every(
    ([url, width], i) => width === element_urls[i][1] && // We need to test both ways because Vite will create an a full URL with
    // `new URL(asset, import.meta.url).href` for the client when `base: './'`, and the
    // relative URLs inside srcset are not automatically resolved to absolute URLs by
    // browsers (in contrast to img.src). This means both SSR and DOM code could
    // contain relative or absolute URLs.
    (src_url_equal(element_urls[i][0], url) || src_url_equal(url, element_urls[i][0]))
  );
}

// ../../../node_modules/svelte/src/internal/client/dom/elements/bindings/input.js
function bind_value(input, get3, set2 = get3) {
  var batches = /* @__PURE__ */ new WeakSet();
  listen_to_event_and_reset_event(input, "input", async (is_reset) => {
    if (dev_fallback_default && input.type === "checkbox") {
      bind_invalid_checkbox_value();
    }
    var value = is_reset ? input.defaultValue : input.value;
    value = is_numberlike_input(input) ? to_number(value) : value;
    set2(value);
    if (current_batch !== null) {
      batches.add(current_batch);
    }
    await tick();
    if (value !== (value = get3())) {
      var start = input.selectionStart;
      var end = input.selectionEnd;
      var length = input.value.length;
      input.value = value ?? "";
      if (end !== null) {
        var new_length = input.value.length;
        if (start === end && end === length && new_length > length) {
          input.selectionStart = new_length;
          input.selectionEnd = new_length;
        } else {
          input.selectionStart = start;
          input.selectionEnd = Math.min(end, new_length);
        }
      }
    }
  });
  if (
    // If we are hydrating and the value has since changed,
    // then use the updated value from the input instead.
    hydrating && input.defaultValue !== input.value || // If defaultValue is set, then value == defaultValue
    // TODO Svelte 6: remove input.value check and set to empty string?
    untrack(get3) == null && input.value
  ) {
    set2(is_numberlike_input(input) ? to_number(input.value) : input.value);
    if (current_batch !== null) {
      batches.add(current_batch);
    }
  }
  render_effect(() => {
    if (dev_fallback_default && input.type === "checkbox") {
      bind_invalid_checkbox_value();
    }
    var value = get3();
    if (input === document.activeElement) {
      var batch = (
        /** @type {Batch} */
        async_mode_flag ? previous_batch : current_batch
      );
      if (batches.has(batch)) {
        return;
      }
    }
    if (is_numberlike_input(input) && value === to_number(input.value)) {
      return;
    }
    if (input.type === "date" && !value && !input.value) {
      return;
    }
    if (value !== input.value) {
      input.value = value ?? "";
    }
  });
}
function is_numberlike_input(input) {
  var type = input.type;
  return type === "number" || type === "range";
}
function to_number(value) {
  return value === "" ? null : +value;
}

// ../../../node_modules/svelte/src/internal/client/reactivity/props.js
var spread_props_handler = {
  get(target, key2) {
    let i = target.props.length;
    while (i--) {
      let p = target.props[i];
      if (is_function(p)) p = p();
      if (typeof p === "object" && p !== null && key2 in p) return p[key2];
    }
  },
  set(target, key2, value) {
    let i = target.props.length;
    while (i--) {
      let p = target.props[i];
      if (is_function(p)) p = p();
      const desc = get_descriptor(p, key2);
      if (desc && desc.set) {
        desc.set(value);
        return true;
      }
    }
    return false;
  },
  getOwnPropertyDescriptor(target, key2) {
    let i = target.props.length;
    while (i--) {
      let p = target.props[i];
      if (is_function(p)) p = p();
      if (typeof p === "object" && p !== null && key2 in p) {
        const descriptor = get_descriptor(p, key2);
        if (descriptor && !descriptor.configurable) {
          descriptor.configurable = true;
        }
        return descriptor;
      }
    }
  },
  has(target, key2) {
    if (key2 === STATE_SYMBOL || key2 === LEGACY_PROPS) return false;
    for (let p of target.props) {
      if (is_function(p)) p = p();
      if (p != null && key2 in p) return true;
    }
    return false;
  },
  ownKeys(target) {
    const keys = [];
    for (let p of target.props) {
      if (is_function(p)) p = p();
      if (!p) continue;
      for (const key2 in p) {
        if (!keys.includes(key2)) keys.push(key2);
      }
      for (const key2 of Object.getOwnPropertySymbols(p)) {
        if (!keys.includes(key2)) keys.push(key2);
      }
    }
    return keys;
  }
};
function spread_props(...props) {
  return new Proxy({ props }, spread_props_handler);
}
function prop(props, key2, flags2, fallback2) {
  var runes = !legacy_mode_flag || (flags2 & PROPS_IS_RUNES) !== 0;
  var bindable = (flags2 & PROPS_IS_BINDABLE) !== 0;
  var lazy = (flags2 & PROPS_IS_LAZY_INITIAL) !== 0;
  var fallback_value = (
    /** @type {V} */
    fallback2
  );
  var fallback_dirty = true;
  var fallback_signal = (
    /** @type {Derived<V> | undefined} */
    void 0
  );
  var get_fallback = () => {
    if (lazy && runes) {
      fallback_signal ??= derived(
        /** @type {() => V} */
        fallback2
      );
      return get2(fallback_signal);
    }
    if (fallback_dirty) {
      fallback_dirty = false;
      fallback_value = lazy ? untrack(
        /** @type {() => V} */
        fallback2
      ) : (
        /** @type {V} */
        fallback2
      );
    }
    return fallback_value;
  };
  let setter;
  if (bindable) {
    var is_entry_props = STATE_SYMBOL in props || LEGACY_PROPS in props;
    setter = get_descriptor(props, key2)?.set ?? (is_entry_props && key2 in props ? (v) => props[key2] = v : void 0);
  }
  var initial_value;
  var is_store_sub = false;
  if (bindable) {
    [initial_value, is_store_sub] = capture_store_binding(() => (
      /** @type {V} */
      props[key2]
    ));
  } else {
    initial_value = /** @type {V} */
    props[key2];
  }
  if (initial_value === void 0 && fallback2 !== void 0) {
    initial_value = get_fallback();
    if (setter) {
      if (runes) props_invalid_value(key2);
      setter(initial_value);
    }
  }
  var getter;
  if (runes) {
    getter = () => {
      var value = (
        /** @type {V} */
        props[key2]
      );
      if (value === void 0) return get_fallback();
      fallback_dirty = true;
      return value;
    };
  } else {
    getter = () => {
      var value = (
        /** @type {V} */
        props[key2]
      );
      if (value !== void 0) {
        fallback_value = /** @type {V} */
        void 0;
      }
      return value === void 0 ? fallback_value : value;
    };
  }
  if (runes && (flags2 & PROPS_IS_UPDATED) === 0) {
    return getter;
  }
  if (setter) {
    var legacy_parent = props.$$legacy;
    return (
      /** @type {() => V} */
      (function(value, mutation) {
        if (arguments.length > 0) {
          if (!runes || !mutation || legacy_parent || is_store_sub) {
            setter(mutation ? getter() : value);
          }
          return value;
        }
        return getter();
      })
    );
  }
  var overridden = false;
  var d = ((flags2 & PROPS_IS_IMMUTABLE) !== 0 ? derived : derived_safe_equal)(() => {
    overridden = false;
    return getter();
  });
  if (dev_fallback_default) {
    d.label = key2;
  }
  if (bindable) get2(d);
  var parent_effect = (
    /** @type {Effect} */
    active_effect
  );
  return (
    /** @type {() => V} */
    (function(value, mutation) {
      if (arguments.length > 0) {
        const new_value = mutation ? get2(d) : runes && bindable ? proxy(value) : value;
        set(d, new_value);
        overridden = true;
        if (fallback_value !== void 0) {
          fallback_value = new_value;
        }
        return value;
      }
      if (is_destroying_effect && overridden || (parent_effect.f & DESTROYED) !== 0) {
        return d.v;
      }
      return get2(d);
    })
  );
}

// ../../../node_modules/svelte/src/legacy/legacy-client.js
function createClassComponent(options) {
  return new Svelte4Component(options);
}
var Svelte4Component = class {
  /** @type {any} */
  #events;
  /** @type {Record<string, any>} */
  #instance;
  /**
   * @param {ComponentConstructorOptions & {
   *  component: any;
   * }} options
   */
  constructor(options) {
    var sources = /* @__PURE__ */ new Map();
    var add_source = (key2, value) => {
      var s = mutable_source(value, false, false);
      sources.set(key2, s);
      return s;
    };
    const props = new Proxy(
      { ...options.props || {}, $$events: {} },
      {
        get(target, prop2) {
          return get2(sources.get(prop2) ?? add_source(prop2, Reflect.get(target, prop2)));
        },
        has(target, prop2) {
          if (prop2 === LEGACY_PROPS) return true;
          get2(sources.get(prop2) ?? add_source(prop2, Reflect.get(target, prop2)));
          return Reflect.has(target, prop2);
        },
        set(target, prop2, value) {
          set(sources.get(prop2) ?? add_source(prop2, value), value);
          return Reflect.set(target, prop2, value);
        }
      }
    );
    this.#instance = (options.hydrate ? hydrate : mount)(options.component, {
      target: options.target,
      anchor: options.anchor,
      props,
      context: options.context,
      intro: options.intro ?? false,
      recover: options.recover,
      transformError: options.transformError
    });
    if (!async_mode_flag && (!options?.props?.$$host || options.sync === false)) {
      flushSync();
    }
    this.#events = props.$$events;
    for (const key2 of Object.keys(this.#instance)) {
      if (key2 === "$set" || key2 === "$destroy" || key2 === "$on") continue;
      define_property(this, key2, {
        get() {
          return this.#instance[key2];
        },
        /** @param {any} value */
        set(value) {
          this.#instance[key2] = value;
        },
        enumerable: true
      });
    }
    this.#instance.$set = /** @param {Record<string, any>} next */
    (next2) => {
      Object.assign(props, next2);
    };
    this.#instance.$destroy = () => {
      unmount(this.#instance);
    };
  }
  /** @param {Record<string, any>} props */
  $set(props) {
    this.#instance.$set(props);
  }
  /**
   * @param {string} event
   * @param {(...args: any[]) => any} callback
   * @returns {any}
   */
  $on(event2, callback) {
    this.#events[event2] = this.#events[event2] || [];
    const cb = (...args) => callback.call(this, ...args);
    this.#events[event2].push(cb);
    return () => {
      this.#events[event2] = this.#events[event2].filter(
        /** @param {any} fn */
        (fn) => fn !== cb
      );
    };
  }
  $destroy() {
    this.#instance.$destroy();
  }
};

// ../../../node_modules/svelte/src/internal/client/dom/elements/custom-element.js
var SvelteElement;
if (typeof HTMLElement === "function") {
  SvelteElement = class extends HTMLElement {
    /** The Svelte component constructor */
    $$ctor;
    /** Slots */
    $$s;
    /** @type {any} The Svelte component instance */
    $$c;
    /** Whether or not the custom element is connected */
    $$cn = false;
    /** @type {Record<string, any>} Component props data */
    $$d = {};
    /** `true` if currently in the process of reflecting component props back to attributes */
    $$r = false;
    /** @type {Record<string, CustomElementPropDefinition>} Props definition (name, reflected, type etc) */
    $$p_d = {};
    /** @type {Record<string, EventListenerOrEventListenerObject[]>} Event listeners */
    $$l = {};
    /** @type {Map<EventListenerOrEventListenerObject, Function>} Event listener unsubscribe functions */
    $$l_u = /* @__PURE__ */ new Map();
    /** @type {any} The managed render effect for reflecting attributes */
    $$me;
    /** @type {ShadowRoot | null} The ShadowRoot of the custom element */
    $$shadowRoot = null;
    /**
     * @param {*} $$componentCtor
     * @param {*} $$slots
     * @param {ShadowRootInit | undefined} shadow_root_init
     */
    constructor($$componentCtor, $$slots, shadow_root_init) {
      super();
      this.$$ctor = $$componentCtor;
      this.$$s = $$slots;
      if (shadow_root_init) {
        this.$$shadowRoot = this.attachShadow(shadow_root_init);
      }
    }
    /**
     * @param {string} type
     * @param {EventListenerOrEventListenerObject} listener
     * @param {boolean | AddEventListenerOptions} [options]
     */
    addEventListener(type, listener, options) {
      this.$$l[type] = this.$$l[type] || [];
      this.$$l[type].push(listener);
      if (this.$$c) {
        const unsub = this.$$c.$on(type, listener);
        this.$$l_u.set(listener, unsub);
      }
      super.addEventListener(type, listener, options);
    }
    /**
     * @param {string} type
     * @param {EventListenerOrEventListenerObject} listener
     * @param {boolean | AddEventListenerOptions} [options]
     */
    removeEventListener(type, listener, options) {
      super.removeEventListener(type, listener, options);
      if (this.$$c) {
        const unsub = this.$$l_u.get(listener);
        if (unsub) {
          unsub();
          this.$$l_u.delete(listener);
        }
      }
    }
    async connectedCallback() {
      this.$$cn = true;
      if (!this.$$c) {
        let create_slot = function(name) {
          return (anchor) => {
            const slot2 = create_element("slot");
            if (name !== "default") slot2.name = name;
            append(anchor, slot2);
          };
        };
        await Promise.resolve();
        if (!this.$$cn || this.$$c) {
          return;
        }
        const $$slots = {};
        const existing_slots = get_custom_elements_slots(this);
        for (const name of this.$$s) {
          if (name in existing_slots) {
            if (name === "default" && !this.$$d.children) {
              this.$$d.children = create_slot(name);
              $$slots.default = true;
            } else {
              $$slots[name] = create_slot(name);
            }
          }
        }
        for (const attribute of this.attributes) {
          const name = this.$$g_p(attribute.name);
          if (!(name in this.$$d)) {
            this.$$d[name] = get_custom_element_value(name, attribute.value, this.$$p_d, "toProp");
          }
        }
        for (const key2 in this.$$p_d) {
          if (!(key2 in this.$$d) && this[key2] !== void 0) {
            this.$$d[key2] = this[key2];
            delete this[key2];
          }
        }
        this.$$c = createClassComponent({
          component: this.$$ctor,
          target: this.$$shadowRoot || this,
          props: {
            ...this.$$d,
            $$slots,
            $$host: this
          }
        });
        this.$$me = effect_root(() => {
          render_effect(() => {
            this.$$r = true;
            for (const key2 of object_keys(this.$$c)) {
              if (!this.$$p_d[key2]?.reflect) continue;
              this.$$d[key2] = this.$$c[key2];
              const attribute_value = get_custom_element_value(
                key2,
                this.$$d[key2],
                this.$$p_d,
                "toAttribute"
              );
              if (attribute_value == null) {
                this.removeAttribute(this.$$p_d[key2].attribute || key2);
              } else {
                this.setAttribute(this.$$p_d[key2].attribute || key2, attribute_value);
              }
            }
            this.$$r = false;
          });
        });
        for (const type in this.$$l) {
          for (const listener of this.$$l[type]) {
            const unsub = this.$$c.$on(type, listener);
            this.$$l_u.set(listener, unsub);
          }
        }
        this.$$l = {};
      }
    }
    // We don't need this when working within Svelte code, but for compatibility of people using this outside of Svelte
    // and setting attributes through setAttribute etc, this is helpful
    /**
     * @param {string} attr
     * @param {string} _oldValue
     * @param {string} newValue
     */
    attributeChangedCallback(attr2, _oldValue, newValue) {
      if (this.$$r) return;
      attr2 = this.$$g_p(attr2);
      this.$$d[attr2] = get_custom_element_value(attr2, newValue, this.$$p_d, "toProp");
      this.$$c?.$set({ [attr2]: this.$$d[attr2] });
    }
    disconnectedCallback() {
      this.$$cn = false;
      Promise.resolve().then(() => {
        if (!this.$$cn && this.$$c) {
          this.$$c.$destroy();
          this.$$me();
          this.$$c = void 0;
        }
      });
    }
    /**
     * @param {string} attribute_name
     */
    $$g_p(attribute_name) {
      return object_keys(this.$$p_d).find(
        (key2) => this.$$p_d[key2].attribute === attribute_name || !this.$$p_d[key2].attribute && key2.toLowerCase() === attribute_name
      ) || attribute_name;
    }
  };
}
function get_custom_element_value(prop2, value, props_definition, transform) {
  const type = props_definition[prop2]?.type;
  value = type === "Boolean" && typeof value !== "boolean" ? value != null : value;
  if (!transform || !props_definition[prop2]) {
    return value;
  } else if (transform === "toAttribute") {
    switch (type) {
      case "Object":
      case "Array":
        return value == null ? null : JSON.stringify(value);
      case "Boolean":
        return value ? "" : null;
      case "Number":
        return value == null ? null : value;
      default:
        return value;
    }
  } else {
    switch (type) {
      case "Object":
      case "Array":
        return value && JSON.parse(value);
      case "Boolean":
        return value;
      // conversion already handled above
      case "Number":
        return value != null ? +value : value;
      default:
        return value;
    }
  }
}
function get_custom_elements_slots(element2) {
  const result = {};
  element2.childNodes.forEach((node) => {
    result[
      /** @type {Element} node */
      node.slot || "default"
    ] = true;
  });
  return result;
}
function create_custom_element(Component, props_definition, slots, exports, shadow_root_init, extend) {
  let Class = class extends SvelteElement {
    constructor() {
      super(Component, slots, shadow_root_init);
      this.$$p_d = props_definition;
    }
    static get observedAttributes() {
      return object_keys(props_definition).map(
        (key2) => (props_definition[key2].attribute || key2).toLowerCase()
      );
    }
  };
  object_keys(props_definition).forEach((prop2) => {
    define_property(Class.prototype, prop2, {
      get() {
        return this.$$c && prop2 in this.$$c ? this.$$c[prop2] : this.$$d[prop2];
      },
      set(value) {
        value = get_custom_element_value(prop2, value, props_definition);
        this.$$d[prop2] = value;
        var component2 = this.$$c;
        if (component2) {
          var setter = get_descriptor(component2, prop2)?.get;
          if (setter) {
            component2[prop2] = value;
          } else {
            component2.$set({ [prop2]: value });
          }
        }
      }
    });
  });
  exports.forEach((property) => {
    define_property(Class.prototype, property, {
      get() {
        return this.$$c?.[property];
      }
    });
  });
  if (extend) {
    Class = extend(Class);
  }
  Component.element = /** @type {any} */
  Class;
  return Class;
}

// ../../../node_modules/svelte/src/index-client.js
if (dev_fallback_default) {
  let throw_rune_error = function(rune) {
    if (!(rune in globalThis)) {
      let value;
      Object.defineProperty(globalThis, rune, {
        configurable: true,
        // eslint-disable-next-line getter-return
        get: () => {
          if (value !== void 0) {
            return value;
          }
          rune_outside_svelte(rune);
        },
        set: (v) => {
          value = v;
        }
      });
    }
  };
  throw_rune_error("$state");
  throw_rune_error("$effect");
  throw_rune_error("$derived");
  throw_rune_error("$inspect");
  throw_rune_error("$props");
  throw_rune_error("$bindable");
}
function onMount(fn) {
  if (component_context === null) {
    lifecycle_outside_component("onMount");
  }
  if (legacy_mode_flag && component_context.l !== null) {
    init_update_callbacks(component_context).m.push(fn);
  } else {
    user_effect(() => {
      const cleanup = untrack(fn);
      if (typeof cleanup === "function") return (
        /** @type {() => void} */
        cleanup
      );
    });
  }
}
function onDestroy(fn) {
  if (component_context === null) {
    lifecycle_outside_component("onDestroy");
  }
  onMount(() => () => untrack(fn));
}
function init_update_callbacks(context) {
  var l = (
    /** @type {ComponentContextLegacy} */
    context.l
  );
  return l.u ??= { a: [], b: [], m: [] };
}

// src/theme.ts
var STORAGE_KEY = "openbook-dashboard-theme";
var DARK_QUERY = "(prefers-color-scheme: dark)";
function systemTheme() {
  return window.matchMedia(DARK_QUERY).matches ? "dark" : "light";
}
function storedTheme() {
  const value = localStorage.getItem(STORAGE_KEY);
  return value === "light" || value === "dark" ? value : null;
}
function applyTheme(value) {
  document.documentElement.setAttribute("data-theme", value);
}
var theme = writable(storedTheme() ?? systemTheme());
function setTheme(value) {
  localStorage.setItem(STORAGE_KEY, value);
  applyTheme(value);
  theme.set(value);
}
function toggleTheme() {
  setTheme(get(theme) === "dark" ? "light" : "dark");
}
function initTheme() {
  applyTheme(get(theme));
  window.matchMedia(DARK_QUERY).addEventListener("change", (event2) => {
    if (!storedTheme()) {
      const next2 = event2.matches ? "dark" : "light";
      applyTheme(next2);
      theme.set(next2);
    }
  });
}

// ../../../node_modules/svelte/src/version.js
var PUBLIC_VERSION = "5";

// ../../../node_modules/svelte/src/internal/disclose-version.js
if (typeof window !== "undefined") {
  ((window.__svelte ??= {}).v ??= /* @__PURE__ */ new Set()).add(PUBLIC_VERSION);
}

// ../../../node_modules/svelte/src/internal/flags/async.js
enable_async_mode_flag();

// ../../../node_modules/regexparam/dist/index.mjs
function parse(str, loose) {
  if (str instanceof RegExp) return { keys: false, pattern: str };
  var c, o, tmp, ext, keys = [], pattern = "", arr = str.split("/");
  arr[0] || arr.shift();
  while (tmp = arr.shift()) {
    c = tmp[0];
    if (c === "*") {
      keys.push("wild");
      pattern += "/(.*)";
    } else if (c === ":") {
      o = tmp.indexOf("?", 1);
      ext = tmp.indexOf(".", 1);
      keys.push(tmp.substring(1, !!~o ? o : !!~ext ? ext : tmp.length));
      pattern += !!~o && !~ext ? "(?:/([^/]+?))?" : "/([^/]+?)";
      if (!!~ext) pattern += (!!~o ? "?" : "") + "\\" + tmp.substring(ext);
    } else {
      pattern += "/" + tmp;
    }
  }
  return {
    keys,
    pattern: new RegExp("^" + pattern + (loose ? "(?=$|/)" : "/?$"), "i")
  };
}

// ../../../node_modules/svelte-spa-router/dist/Router.svelte
var RouterStateImpl = class {
  #_loc = (
    /** The current full location (incl. querystring) */
    state(getLocation())
  );
  get _loc() {
    return get2(this.#_loc);
  }
  set _loc(value) {
    set(this.#_loc, value);
  }
  #_location = user_derived(() => this._loc.location);
  get _location() {
    return get2(this.#_location);
  }
  set _location(value) {
    set(this.#_location, value);
  }
  #_querystring = user_derived(() => this._loc.querystring);
  get _querystring() {
    return get2(this.#_querystring);
  }
  set _querystring(value) {
    set(this.#_querystring, value);
  }
  #_params = state(void 0);
  get _params() {
    return get2(this.#_params);
  }
  set _params(value) {
    set(this.#_params, value);
  }
  get loc() {
    return this._loc;
  }
  /** The current location (excluding querystring) */
  get location() {
    return this._location;
  }
  /** The current querystring */
  get querystring() {
    return this._querystring;
  }
  get params() {
    return this._params;
  }
  constructor() {
    window.addEventListener("hashchange", () => {
      this._loc = getLocation();
    });
  }
};
var router = new RouterStateImpl();
function getLocation() {
  const hashPosition = window.location.href.indexOf("#/");
  let location = hashPosition > -1 ? window.location.href.substr(hashPosition + 1) : "/";
  const qsPosition = location.indexOf("?");
  let querystring = "";
  if (qsPosition > -1) {
    querystring = location.substr(qsPosition + 1);
    location = location.substr(0, qsPosition);
  }
  return { location, querystring };
}
async function push2(location) {
  if (!location || location.length < 1 || location.charAt(0) != "/" && location.indexOf("#/") !== 0) {
    throw Error("Invalid parameter location");
  }
  await tick();
  history.replaceState(
    {
      ...history.state,
      __svelte_spa_router_scrollX: window.scrollX,
      __svelte_spa_router_scrollY: window.scrollY
    },
    ""
  );
  window.location.hash = (location.charAt(0) == "#" ? "" : "#") + location;
}
function restoreScroll(state3) {
  if (state3) {
    window.scrollTo(state3.__svelte_spa_router_scrollX || 0, state3.__svelte_spa_router_scrollY || 0);
  } else {
    window.scrollTo(0, 0);
  }
}
function Router($$anchor, $$props) {
  push($$props, true);
  const routes = prop($$props, "routes", 23, () => ({})), prefix = prop($$props, "prefix", 7, ""), restoreScrollState = prop($$props, "restoreScrollState", 7, false), onConditionsFailed = prop($$props, "onConditionsFailed", 7, () => {
  }), onRouteLoaded = prop($$props, "onRouteLoaded", 7, () => {
  }), onRouteLoading = prop($$props, "onRouteLoading", 7, () => {
  }), onRouteEvent = prop($$props, "onRouteEvent", 7, () => {
  });
  class RouteItem {
    path;
    component;
    conditions;
    userData;
    props;
    _pattern;
    _keys;
    constructor(path, component3) {
      const isWrapped = (c) => typeof c == "object" && c !== null && c._sveltesparouter === true;
      if (!component3 || typeof component3 != "function" && !isWrapped(component3)) {
        throw Error("Invalid component object");
      }
      if (!path || typeof path == "string" && (path.length < 1 || path.charAt(0) != "/" && path.charAt(0) != "*") || typeof path == "object" && !(path instanceof RegExp)) {
        throw Error('Invalid value for "path" argument - strings must start with / or *');
      }
      const parsed = typeof path == "string" ? parse(path) : parse(path);
      this.path = path;
      if (isWrapped(component3)) {
        const wrapped = component3;
        this.component = wrapped.component;
        this.conditions = wrapped.conditions || [];
        this.userData = wrapped.userData;
        this.props = wrapped.props || {};
      } else {
        const sync = component3;
        this.component = () => Promise.resolve(sync);
        this.conditions = [];
        this.props = {};
      }
      this._pattern = parsed.pattern;
      this._keys = parsed.keys;
    }
    /**
     * Checks if `path` matches the current route.
     * Returns the list of parameters from the URL, or `null` if no match.
     */
    match(path) {
      if (prefix()) {
        if (typeof prefix() == "string") {
          if (path.startsWith(prefix())) {
            path = path.substr(prefix().length) || "/";
          } else {
            return null;
          }
        } else if (prefix() instanceof RegExp) {
          const m = path.match(prefix());
          if (m && m[0]) {
            path = path.substr(m[0].length) || "/";
          } else {
            return null;
          }
        }
      }
      const matches = this._pattern.exec(path);
      if (matches === null) {
        return null;
      }
      if (this._keys === false) {
        return matches;
      }
      const out = {};
      let i = 0;
      while (i < this._keys.length) {
        try {
          out[this._keys[i]] = decodeURIComponent(matches[i + 1] || "") || null;
        } catch {
          out[this._keys[i]] = null;
        }
        i++;
      }
      return out;
    }
    /** Executes all conditions in order; returns false at the first failure. */
    async checkConditions(detail) {
      for (let i = 0; i < this.conditions.length; i++) {
        if (!await this.conditions[i](detail)) {
          return false;
        }
      }
      return true;
    }
  }
  const routesList = [];
  if (routes() instanceof Map) {
    routes().forEach((route, path) => {
      routesList.push(new RouteItem(path, route));
    });
  } else {
    Object.keys(routes()).forEach((path) => {
      const map = routes();
      routesList.push(new RouteItem(path, map[path]));
    });
  }
  let component2 = state(null);
  let componentParams = state(null);
  let routeProps = state({});
  let previousScrollState = null;
  let componentObj = null;
  user_effect(() => {
    history.scrollRestoration = restoreScrollState() ? "manual" : "auto";
  });
  user_effect(() => {
    if (!restoreScrollState()) {
      return;
    }
    const popStateChanged = (event2) => {
      if (event2.state && (event2.state.__svelte_spa_router_scrollY || event2.state.__svelte_spa_router_scrollX)) {
        previousScrollState = event2.state;
      } else {
        previousScrollState = null;
      }
    };
    window.addEventListener("popstate", popStateChanged);
    return () => window.removeEventListener("popstate", popStateChanged);
  });
  async function dispatchNextTick(event2, detail) {
    await tick();
    event2(detail);
  }
  user_effect(() => {
    const newLoc = router.loc;
    let cancelled = false;
    untrack(async () => {
      let i = 0;
      while (i < routesList.length) {
        const match = routesList[i].match(newLoc.location);
        if (!match) {
          i++;
          continue;
        }
        const matchParams = matchToParams(match);
        const detail = {
          route: routesList[i].path,
          location: newLoc.location,
          querystring: newLoc.querystring || "",
          userData: routesList[i].userData,
          params: matchParams
        };
        if (!await routesList[i].checkConditions(detail)) {
          if (cancelled) {
            return;
          }
          set(component2, null);
          componentObj = null;
          dispatchNextTick(onConditionsFailed(), detail);
          return;
        }
        if (cancelled) {
          return;
        }
        dispatchNextTick(onRouteLoading(), { ...detail });
        const obj = routesList[i].component;
        if (componentObj != obj) {
          if (obj.loading) {
            set(component2, obj.loading);
            componentObj = obj;
            set(componentParams, obj.loadingParams || null);
            set(routeProps, {});
            const comp2 = obj.loading;
            dispatchNextTick(onRouteLoaded(), {
              ...detail,
              component: comp2,
              name: comp2.name,
              params: obj.loadingParams || null
            });
          } else {
            set(component2, null);
            componentObj = null;
          }
          const loaded = await obj();
          if (cancelled) {
            return;
          }
          set(component2, loaded && typeof loaded == "object" && "default" in loaded ? loaded.default : loaded);
          componentObj = obj;
        }
        set(componentParams, matchParams);
        set(routeProps, routesList[i].props);
        const comp = get2(component2);
        if (comp) {
          dispatchNextTick(onRouteLoaded(), {
            ...detail,
            component: comp,
            name: comp.name,
            params: matchParams
          });
        }
        router._params = matchParams;
        if (restoreScrollState()) {
          restoreScroll(previousScrollState);
          previousScrollState = null;
        }
        return;
      }
      set(component2, null);
      componentObj = null;
      router._params = void 0;
      if (restoreScrollState()) {
        restoreScroll(previousScrollState);
        previousScrollState = null;
      }
    });
    return () => {
      cancelled = true;
    };
  });
  function matchToParams(match) {
    return match && typeof match == "object" && Object.keys(match).length ? match : null;
  }
  var $$exports = {
    get routes() {
      return routes();
    },
    set routes($$value = {}) {
      routes($$value);
      flushSync();
    },
    get prefix() {
      return prefix();
    },
    set prefix($$value = "") {
      prefix($$value);
      flushSync();
    },
    get restoreScrollState() {
      return restoreScrollState();
    },
    set restoreScrollState($$value = false) {
      restoreScrollState($$value);
      flushSync();
    },
    get onConditionsFailed() {
      return onConditionsFailed();
    },
    set onConditionsFailed($$value = () => {
    }) {
      onConditionsFailed($$value);
      flushSync();
    },
    get onRouteLoaded() {
      return onRouteLoaded();
    },
    set onRouteLoaded($$value = () => {
    }) {
      onRouteLoaded($$value);
      flushSync();
    },
    get onRouteLoading() {
      return onRouteLoading();
    },
    set onRouteLoading($$value = () => {
    }) {
      onRouteLoading($$value);
      flushSync();
    },
    get onRouteEvent() {
      return onRouteEvent();
    },
    set onRouteEvent($$value = () => {
    }) {
      onRouteEvent($$value);
      flushSync();
    }
  };
  var fragment = comment();
  var node_1 = first_child(fragment);
  {
    var consequent_1 = ($$anchor2) => {
      const Component = user_derived(() => get2(component2));
      var fragment_1 = comment();
      var node_2 = first_child(fragment_1);
      {
        var consequent = ($$anchor3) => {
          var fragment_2 = comment();
          var node_3 = first_child(fragment_2);
          component(node_3, () => get2(Component), ($$anchor4, Component_1) => {
            Component_1($$anchor4, spread_props(
              {
                get params() {
                  return get2(componentParams);
                },
                get onRouteEvent() {
                  return onRouteEvent();
                }
              },
              () => get2(routeProps)
            ));
          });
          append($$anchor3, fragment_2);
        };
        var alternate = ($$anchor3) => {
          var fragment_3 = comment();
          var node_4 = first_child(fragment_3);
          component(node_4, () => get2(Component), ($$anchor4, Component_2) => {
            Component_2($$anchor4, spread_props(
              {
                get onRouteEvent() {
                  return onRouteEvent();
                }
              },
              () => get2(routeProps)
            ));
          });
          append($$anchor3, fragment_3);
        };
        if_block(node_2, ($$render) => {
          if (get2(componentParams)) $$render(consequent);
          else $$render(alternate, -1);
        });
      }
      append($$anchor2, fragment_1);
    };
    if_block(node_1, ($$render) => {
      if (get2(component2)) $$render(consequent_1);
    });
  }
  append($$anchor, fragment);
  return pop($$exports);
}
create_custom_element(
  Router,
  {
    routes: {},
    prefix: {},
    restoreScrollState: {},
    onConditionsFailed: {},
    onRouteLoaded: {},
    onRouteLoading: {},
    onRouteEvent: {}
  },
  [],
  [],
  { mode: "open" }
);

// src/api/websocket.ts
var MAX_ATTEMPTS = 5;
var BASE_DELAY_MS = 250;
var STABLE_CONNECTION_MS = 4e3;
var MAX_UNSTABLE_RETRIES = 4;
var WebSocketServerError = class extends Error {
  payload;
  constructor(message, payload = [], cause) {
    super(message, { cause });
    this.name = "WebSocketServerError";
    this.payload = payload;
  }
};
function isWebSocketServerErrorMessage(message) {
  return typeof message === "object" && message !== null && "action" in message && message.action === "error";
}
function formatServerError(payload) {
  if (!Array.isArray(payload) || payload.length === 0) {
    return "Unknown WebSocket error.";
  }
  return payload.map(({ type, msg, loc }) => {
    const reason = msg || "Unknown WebSocket error.";
    const suffix = Array.isArray(loc) && loc.length ? ` (${loc.map(String).join(".")})` : "";
    return type ? `${reason} [${type}]${suffix}` : `${reason}${suffix}`;
  }).join("\n");
}
var WebSocketClient = class {
  #url;
  #socket;
  #status = "disconnected";
  #statusListener;
  #errorHandler;
  #messageHandlers = /* @__PURE__ */ new Map();
  #messageQueue = [];
  #openedAt = 0;
  #unstableRetries = 0;
  constructor(url) {
    this.#url = url;
  }
  /** Register a listener for connection status changes (replaces the previous one). */
  setConnectionStatusListener(listener) {
    this.#statusListener = listener;
  }
  /** Register a handler for generic WebSocket errors (replaces the previous one). */
  setErrorHandler(handler) {
    this.#errorHandler = handler;
  }
  /** Register a handler for a given received message `action` (replaces the previous one). */
  setMessageHandler(action2, handler) {
    this.#messageHandlers.set(action2, handler);
  }
  async #setConnectionStatus(status, reconnectInSec = 0) {
    this.#status = status;
    if (this.#statusListener) {
      await this.#statusListener(status, reconnectInSec);
    }
  }
  /**
   * Connect to the server, retrying up to `MAX_ATTEMPTS` times with increasing
   * delays. Throws if the connection cannot be established.
   */
  async connect() {
    if (this.#status !== "disconnected") {
      return;
    }
    let lastError = null;
    let delayMs = BASE_DELAY_MS;
    for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
      lastError = null;
      try {
        await this.#setConnectionStatus("connecting");
        await new Promise((resolve, reject) => {
          this.#socket = new WebSocket(this.#url);
          this.#socket.addEventListener("open", async () => {
            this.#openedAt = Date.now();
            await this.#setConnectionStatus("connected");
            for (const message of this.#messageQueue) {
              await this.#send(message);
            }
            this.#messageQueue = [];
            resolve(void 0);
          });
          this.#socket.addEventListener("close", () => {
            this.#socket = void 0;
            if (this.#status === "connecting") {
              reject(new Error("WebSocket connection failed."));
              return;
            }
            if (this.#status === "disconnected") {
              return;
            }
            const uptime = Date.now() - this.#openedAt;
            window.setTimeout(async () => {
              await this.#setConnectionStatus("disconnected");
              if (uptime < STABLE_CONNECTION_MS) {
                this.#unstableRetries++;
                if (this.#unstableRetries > MAX_UNSTABLE_RETRIES) {
                  if (this.#errorHandler) {
                    await this.#errorHandler(
                      new Error("The assistant keeps dropping the connection. Please try again later.")
                    );
                  }
                  return;
                }
                await new Promise((r) => setTimeout(r, BASE_DELAY_MS * 2 ** this.#unstableRetries));
              } else {
                this.#unstableRetries = 0;
              }
              try {
                await this.connect();
              } catch (error) {
                console.error(error);
                if (this.#errorHandler) {
                  await this.#errorHandler(error);
                }
              }
            }, 0);
          });
          this.#socket.addEventListener("error", async (error) => {
            console.error(error);
            if (this.#errorHandler) {
              await this.#errorHandler(error);
            }
          });
          this.#socket.addEventListener("message", async (event2) => {
            try {
              const message = JSON.parse(event2.data);
              if (!message.action) {
                throw new Error("Received a WebSocket message without an `action`.");
              }
              if (isWebSocketServerErrorMessage(message)) {
                const error = new WebSocketServerError(
                  formatServerError(message.payload),
                  message.payload ?? [],
                  message
                );
                console.error(error);
                if (this.#errorHandler) {
                  await this.#errorHandler(error);
                }
                return;
              }
              const handler = this.#messageHandlers.get(message.action);
              if (!handler) {
                console.warn('No handler for WebSocket action "%s".', message.action, message);
                return;
              }
              await handler(message);
            } catch (error) {
              console.error(error);
              if (this.#errorHandler) {
                await this.#errorHandler(error);
              }
            }
          });
        });
      } catch (error) {
        lastError = error;
      }
      if (this.#status === "connected") {
        return;
      }
      await this.#setConnectionStatus("wait_before_retry", delayMs / 1e3);
      await new Promise((resolve) => setTimeout(resolve, delayMs));
      delayMs *= 2;
      console.warn(`WebSocket retry ${attempt}/${MAX_ATTEMPTS} for ${this.#url}.`);
    }
    await this.#setConnectionStatus("disconnected");
    if (lastError instanceof Error) {
      throw lastError;
    }
    throw new Error("WebSocket connection failed.");
  }
  /** Disconnect and stop reconnecting until `connect()` is called again. */
  async disconnect() {
    if (!this.#socket) {
      return;
    }
    await this.#setConnectionStatus("disconnected");
    this.#socket.close();
  }
  /** Reset the unstable-connection counter and try connecting again. */
  async retry() {
    this.#unstableRetries = 0;
    await this.connect();
  }
  /** Send a message, or queue it until the connection is (re)established. */
  async send(message) {
    if (this.#status === "connected" && this.#socket) {
      await this.#send(message);
    } else {
      this.#messageQueue.push(message);
    }
  }
  async #send(message) {
    if (!this.#socket) {
      return;
    }
    this.#socket.send(JSON.stringify(message));
  }
};

// src/api/client.ts
var baseUrlPromise = null;
function isLoopbackHost(hostname) {
  return hostname === "localhost" || hostname === "127.0.0.1" || hostname === "::1";
}
function normalizeBaseUrl(value) {
  let configuredUrl = new URL(value || window.location.origin, window.location.origin);
  const currentUrl = new URL(window.location.origin);
  if (isLoopbackHost(configuredUrl.hostname) && isLoopbackHost(currentUrl.hostname) && configuredUrl.protocol === currentUrl.protocol && configuredUrl.port === currentUrl.port) {
    configuredUrl = currentUrl;
  }
  let url = configuredUrl.toString();
  while (url.endsWith("/")) {
    url = url.slice(0, url.length - 1);
  }
  return url;
}
async function resolveBaseUrl() {
  const response = await fetch("server.url");
  if (!response.ok) {
    throw new Error(`Could not load backend URL (HTTP ${response.status}).`);
  }
  return normalizeBaseUrl((await response.text()).trim());
}
function getBaseUrl() {
  if (!baseUrlPromise) {
    baseUrlPromise = resolveBaseUrl();
  }
  return baseUrlPromise;
}
async function ws(suffix) {
  const path = suffix.startsWith("/") ? suffix : `/${suffix}`;
  const wsUrl = new URL(`/ws${path}`, `${await getBaseUrl()}/`);
  if (wsUrl.protocol === "http:") {
    wsUrl.protocol = "ws:";
  } else if (wsUrl.protocol === "https:") {
    wsUrl.protocol = "wss:";
  }
  return new WebSocketClient(wsUrl.toString());
}
async function apiGet(path, query = {}) {
  const base = await getBaseUrl();
  const url = new URL(`${base}${path}`);
  for (const [key2, value] of Object.entries(query)) {
    url.searchParams.set(key2, value);
  }
  const response = await fetch(url.toString(), {
    credentials: "include",
    headers: { Accept: "application/json" }
  });
  if (response.status === 401 || response.status === 403) {
    throw new Error("You are not signed in. Please log in to view your dashboard.");
  }
  if (!response.ok) {
    throw new Error(`Request to ${path} failed (HTTP ${response.status}).`);
  }
  return await response.json();
}
function readCookie(name) {
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  const value = match?.[1];
  return value ? decodeURIComponent(value) : "";
}
function extractError(data) {
  if (typeof data === "string") {
    return data;
  }
  if (data && typeof data === "object") {
    const record = data;
    if (typeof record.detail === "string") {
      return record.detail;
    }
    if (Array.isArray(record.errors)) {
      const messages = record.errors.map((entry) => entry && typeof entry === "object" ? String(entry.message ?? "") : "").filter(Boolean);
      if (messages.length > 0) {
        return messages.join(" ");
      }
    }
    const fieldMessages = Object.values(record).flatMap((value) => Array.isArray(value) ? value : [value]).filter((value) => typeof value === "string");
    if (fieldMessages.length > 0) {
      return fieldMessages.join(" ");
    }
  }
  return "";
}
async function apiSend(method, path, body, options = {}) {
  const base = await getBaseUrl();
  const headers = {
    Accept: "application/json",
    "X-CSRFToken": readCookie("csrftoken")
  };
  let payload;
  if (options.formData && body instanceof FormData) {
    payload = body;
  } else if (body !== void 0) {
    headers["Content-Type"] = "application/json";
    payload = JSON.stringify(body);
  }
  const response = await fetch(`${base}${path}`, {
    method,
    credentials: "include",
    headers,
    body: payload
  });
  if (!response.ok) {
    const data = await response.json().catch(() => null);
    throw new Error(extractError(data) || `Request to ${path} failed (HTTP ${response.status}).`);
  }
  if (response.status === 204) {
    return void 0;
  }
  return await response.json().catch(() => void 0);
}

// src/api/gamification.ts
function toList(data) {
  return Array.isArray(data) ? data : data.results;
}
function fetchAccountProgress() {
  return apiGet("/api/gamification/account_progress/me/");
}
async function fetchStreak() {
  const data = await apiGet("/api/gamification/streak/");
  if (Array.isArray(data)) {
    return data[0] ?? null;
  }
  if ("results" in data) {
    return data.results[0] ?? null;
  }
  return data;
}
async function fetchSkillProgress(username) {
  const query = { _expand: "skill", _page_size: "100", _sort: "skill__name" };
  if (username) {
    query.account = username;
  }
  const data = await apiGet(
    "/api/gamification/skill_progress/",
    query
  );
  return toList(data);
}
async function fetchCourseProgress(username) {
  const query = { _expand: "course", _page_size: "100", _sort: "course__name" };
  if (username) {
    query.account = username;
  }
  const data = await apiGet(
    "/api/gamification/course_progress/",
    query
  );
  return toList(data);
}
async function fetchCurrentUser() {
  const data = await apiGet(
    "/api/auth/current_user/"
  );
  if (Array.isArray(data)) {
    return data[0] ?? null;
  }
  if ("results" in data) {
    return data.results[0] ?? null;
  }
  return data;
}

// src/data/dashboard.ts
function toNumber(value, fallback2 = 0) {
  const numeric = typeof value === "number" ? value : Number(value);
  return Number.isFinite(numeric) ? numeric : fallback2;
}
function clampPercent(value) {
  return Math.min(100, Math.max(0, value));
}
function mapUser(user) {
  if (!user) {
    return null;
  }
  return {
    username: user.username,
    fullName: user.full_name || user.username,
    avatarUrl: user.picture ?? null,
    isAuthenticated: Boolean(user.is_authenticated)
  };
}
function levelProgress(points, progress) {
  const currentMin = toNumber(progress?.current_level_min_points);
  const nextMin = progress?.next_level_min_points;
  if (nextMin === null || nextMin === void 0) {
    return 100;
  }
  const span = nextMin - currentMin;
  return span > 0 ? clampPercent((points - currentMin) / span * 100) : 0;
}
function mapStats(progress, streak) {
  if (!progress && !streak) {
    return null;
  }
  const points = toNumber(progress?.point_total);
  return {
    points,
    level: toNumber(progress?.level, 1),
    levelProgress: levelProgress(points, progress),
    nextLevelPoints: progress?.next_level_min_points ?? null,
    currentStreak: toNumber(streak?.current_streak),
    longestStreak: toNumber(streak?.longest_streak),
    streakFreezes: toNumber(streak?.streak_freezes),
    lastActiveDate: streak?.last_active_date ? new Date(streak.last_active_date) : null
  };
}
function skillName(skill) {
  if (typeof skill === "string") {
    return { name: skill, iconPath: "" };
  }
  return { name: skill.name, iconPath: skill.icon_path ?? "" };
}
function mapSkills(records) {
  return records.map((record) => {
    const { name, iconPath } = skillName(record.skill);
    return {
      id: record.id,
      name,
      iconPath,
      level: toNumber(record.level, 1),
      progress: clampPercent(toNumber(record.progress))
    };
  });
}
function courseName(course) {
  return typeof course === "string" ? course : course.name;
}
function mapCourses(records) {
  return records.map((record) => ({
    id: record.id,
    name: courseName(record.course),
    level: toNumber(record.course_level, 1),
    points: toNumber(record.course_points),
    progress: clampPercent(toNumber(record.course_progress))
  }));
}
async function loadDashboardData() {
  const user = await fetchCurrentUser();
  const username = user?.username ?? null;
  const [progress, streak, skills, courses] = await Promise.all([
    fetchAccountProgress(),
    fetchStreak(),
    fetchSkillProgress(username),
    fetchCourseProgress(username)
  ]);
  const ownSkills = username ? skills.filter((record) => record.account === username) : skills;
  const ownCourses = username ? courses.filter((record) => record.account === username) : courses;
  return {
    user: mapUser(user),
    stats: mapStats(progress, streak),
    skills: mapSkills(ownSkills),
    courses: mapCourses(ownCourses)
  };
}

// src/stores/dashboard.store.ts
var initialState = {
  isLoading: true,
  errorMessage: "",
  user: null,
  stats: null,
  skills: [],
  courses: []
};
var state2 = writable(initialState);
function toMessage(error) {
  return error instanceof Error ? error.message : String(error);
}
async function refresh() {
  state2.update((current) => ({ ...current, isLoading: true, errorMessage: "" }));
  try {
    const data = await loadDashboardData();
    state2.set({ isLoading: false, errorMessage: "", ...data });
  } catch (error) {
    state2.update((current) => ({ ...current, isLoading: false, errorMessage: toMessage(error) }));
  }
}
var dashboardStore = {
  subscribe: state2.subscribe,
  refresh
};

// src/components/app-frame/DashboardHeader.svelte
var root = from_html(`<img alt="" class="svelte-1xhay2l"/>`);
var root_1 = from_html(`<header class="app-header svelte-1xhay2l"><div class="header-left svelte-1xhay2l"><img class="brand-logo svelte-1xhay2l"/> <span class="brand-text svelte-1xhay2l"> </span></div> <div class="header-right svelte-1xhay2l"><button type="button" class="theme-toggle svelte-1xhay2l"> </button> <span class="avatar-mark svelte-1xhay2l" aria-hidden="true"><!></span> <span class="page-label svelte-1xhay2l"> </span> <span class="status-pill svelte-1xhay2l"><span class="status-dot svelte-1xhay2l" aria-hidden="true"></span> </span></div></header>`);
var $$css = {
  hash: "svelte-1xhay2l",
  code: ".app-header.svelte-1xhay2l {position:sticky;top:0;z-index:50;display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:0.75rem 1.5rem;background:var(--color-base-100);border-bottom:1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);}.header-left.svelte-1xhay2l {display:flex;align-items:center;gap:0.75rem;font-weight:700;letter-spacing:0.05em;}.brand-logo.svelte-1xhay2l {width:2.4rem;height:2.4rem;border-radius:0.6rem;object-fit:contain;}.brand-text.svelte-1xhay2l {font-size:1.05rem;text-transform:uppercase;color:var(--color-base-content);}.header-right.svelte-1xhay2l {display:flex;align-items:center;gap:0.85rem;}.theme-toggle.svelte-1xhay2l {display:grid;place-items:center;width:2rem;height:2rem;border-radius:999px;font-size:1rem;cursor:pointer;background:color-mix(in oklab, var(--color-base-200) 70%, transparent);border:1px solid color-mix(in oklab, var(--color-base-content) 18%, transparent);}.theme-toggle.svelte-1xhay2l:hover {border-color:color-mix(in oklab, var(--color-primary) 50%, transparent);}.theme-toggle.svelte-1xhay2l:focus-visible {outline:2px solid var(--color-primary);outline-offset:2px;}.avatar-mark.svelte-1xhay2l {width:1.9rem;height:1.9rem;border-radius:999px;overflow:hidden;background:color-mix(in oklab, var(--color-base-content) 18%, transparent);}.avatar-mark.svelte-1xhay2l img:where(.svelte-1xhay2l) {width:100%;height:100%;object-fit:cover;}.page-label.svelte-1xhay2l {font-size:0.9rem;color:var(--color-primary);}.status-pill.svelte-1xhay2l {display:inline-flex;align-items:center;gap:0.5rem;padding:0.35rem 0.75rem;border-radius:999px;border:1px solid color-mix(in oklab, var(--color-base-content) 18%, transparent);font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;background:color-mix(in oklab, var(--color-base-200) 70%, transparent);color:color-mix(in oklab, var(--color-base-content) 80%, transparent);}.status-dot.svelte-1xhay2l {width:0.5rem;height:0.5rem;border-radius:999px;background:var(--color-success);box-shadow:0 0 12px color-mix(in oklab, var(--color-success) 70%, transparent);}\r\n\r\n    @media (max-width: 40rem) {.app-header.svelte-1xhay2l {flex-direction:column;gap:0.75rem;text-align:center;}\r\n    }"
};
function DashboardHeader($$anchor, $$props) {
  push($$props, true);
  append_styles($$anchor, $$css);
  const $theme = () => store_get(theme, "$theme", $$stores);
  const [$$stores, $$cleanup] = setup_stores();
  let user = prop($$props, "user", 7, null), brand = prop($$props, "brand", 7, "ElisaAI"), logoSrc = prop($$props, "logoSrc", 7, "logo.png"), pageLabel = prop($$props, "pageLabel", 7, "Dashboard"), statusLabel = prop($$props, "statusLabel", 7, "System online"), statusDetail = prop($$props, "statusDetail", 7, "v2.0.2.5");
  var $$exports = {
    get user() {
      return user();
    },
    set user($$value = null) {
      user($$value);
      flushSync();
    },
    get brand() {
      return brand();
    },
    set brand($$value = "ElisaAI") {
      brand($$value);
      flushSync();
    },
    get logoSrc() {
      return logoSrc();
    },
    set logoSrc($$value = "logo.png") {
      logoSrc($$value);
      flushSync();
    },
    get pageLabel() {
      return pageLabel();
    },
    set pageLabel($$value = "Dashboard") {
      pageLabel($$value);
      flushSync();
    },
    get statusLabel() {
      return statusLabel();
    },
    set statusLabel($$value = "System online") {
      statusLabel($$value);
      flushSync();
    },
    get statusDetail() {
      return statusDetail();
    },
    set statusDetail($$value = "v2.0.2.5") {
      statusDetail($$value);
      flushSync();
    }
  };
  var header = root_1();
  var div = child(header);
  var img = child(div);
  var span = sibling(img, 2);
  var text2 = child(span, true);
  reset(span);
  reset(div);
  var div_1 = sibling(div, 2);
  var button = child(div_1);
  var text_1 = child(button, true);
  reset(button);
  var span_1 = sibling(button, 2);
  var node = child(span_1);
  {
    var consequent = ($$anchor2) => {
      var img_1 = root();
      template_effect(() => set_attribute2(img_1, "src", user().avatarUrl));
      append($$anchor2, img_1);
    };
    if_block(node, ($$render) => {
      if (user()?.avatarUrl) $$render(consequent);
    });
  }
  reset(span_1);
  var span_2 = sibling(span_1, 2);
  var text_2 = child(span_2, true);
  reset(span_2);
  var span_3 = sibling(span_2, 2);
  var text_3 = sibling(child(span_3));
  reset(span_3);
  reset(div_1);
  reset(header);
  template_effect(() => {
    set_attribute2(img, "src", logoSrc());
    set_attribute2(img, "alt", `${brand()} logo`);
    set_text(text2, brand());
    set_attribute2(button, "aria-label", $theme() === "dark" ? "Switch to light mode" : "Switch to dark mode");
    set_text(text_1, $theme() === "dark" ? "\u2600\uFE0F" : "\u{1F319}");
    set_text(text_2, pageLabel());
    set_text(text_3, ` ${statusLabel() ?? ""} // ${statusDetail() ?? ""}`);
  });
  delegated("click", button, function(...$$args) {
    toggleTheme?.apply(this, $$args);
  });
  append($$anchor, header);
  var $$pop = pop($$exports);
  $$cleanup();
  return $$pop;
}
delegate(["click"]);
create_custom_element(
  DashboardHeader,
  {
    user: {},
    brand: {},
    logoSrc: {},
    pageLabel: {},
    statusLabel: {},
    statusDetail: {}
  },
  [],
  [],
  { mode: "open" }
);

// src/stores/ai-chat.store.ts
function createAiChatStore(courseId) {
  const { subscribe, update: update2 } = writable({
    connection: "disconnected",
    errorMessage: "",
    messages: []
  });
  let socket;
  const endpoint = courseId ? `/ai/courses/${encodeURIComponent(courseId)}/chat` : "/ai/chat";
  async function getChatHistory() {
    await socket?.send({ action: "get_chat_history", payload: null });
  }
  async function connect() {
    if (!socket) {
      socket = await ws(endpoint);
      socket.setConnectionStatusListener((status) => {
        update2((state3) => ({
          ...state3,
          connection: status,
          errorMessage: status === "connected" ? "" : state3.errorMessage
        }));
        if (status === "connected") {
          void getChatHistory();
        }
      });
      socket.setErrorHandler((error) => {
        const message = error instanceof Error ? error.message : "WebSocket error.";
        update2((state3) => ({ ...state3, errorMessage: message }));
      });
      socket.setMessageHandler("chat_history", (message) => {
        update2((state3) => ({ ...state3, messages: message.payload.messages }));
      });
      socket.setMessageHandler("chat_message", (message) => {
        update2((state3) => {
          const index2 = state3.messages.findIndex((m) => m.id === message.payload.id);
          const messages = index2 === -1 ? [...state3.messages, message.payload] : state3.messages.map((m, i) => i === index2 ? message.payload : m);
          return { ...state3, messages };
        });
      });
    }
    await socket.connect();
  }
  async function disconnect() {
    await socket?.disconnect();
  }
  async function retry() {
    update2((state3) => ({ ...state3, errorMessage: "" }));
    if (socket) {
      await socket.retry();
    } else {
      await connect();
    }
  }
  async function sendChatInput(format, content) {
    await socket?.send({ action: "chat_input", payload: { format, content } });
  }
  return { subscribe, connect, disconnect, retry, getChatHistory, sendChatInput };
}

// src/components/app-frame/ChatWidget.svelte
var root2 = from_html(`<img class="avatar svelte-13e87sq" src="logo.png" alt="ElisaAI"/>`);
var root_12 = from_html(`<div><!> <div> </div></div>`);
var root_2 = from_html(`<span class="coming-soon svelte-13e87sq"> </span>`);
var root_3 = from_html(`<section><header class="panel-header svelte-13e87sq" role="toolbar" tabindex="-1" aria-label="Chat window controls"><span class="panel-title svelte-13e87sq"> </span> <div class="panel-actions svelte-13e87sq"><button type="button" class="icon-btn svelte-13e87sq"> </button> <button type="button" class="icon-btn svelte-13e87sq" aria-label="Close chat">\u2715</button></div></header> <div class="panel-body svelte-13e87sq"><div class="message svelte-13e87sq"><img class="avatar svelte-13e87sq" src="logo.png" alt="ElisaAI"/> <div class="bubble svelte-13e87sq">System online. I am <strong>ElisaAI</strong>. Ready to process your queries.
                    What topic shall we analyse today?</div></div> <!></div> <div class="composer svelte-13e87sq"><!> <form class="composer-row svelte-13e87sq"><button type="button" class="composer-add svelte-13e87sq" aria-label="Add" disabled="">+</button> <input class="composer-input svelte-13e87sq" type="text" placeholder="Message"/> <button type="submit" class="composer-send svelte-13e87sq" aria-label="Send">\u2192</button></form> <p class="disclaimer svelte-13e87sq">ElisaAI may generate misinformation. Please verify all information.</p></div></section>`);
var root_4 = from_html(`<!> <button type="button" aria-label="Open Quick Chat"><img src="logo.png" alt="" class="svelte-13e87sq"/></button>`, 1);
var $$css2 = {
  hash: "svelte-13e87sq",
  code: ".fab.svelte-13e87sq {position:fixed;right:1.5rem;bottom:1.5rem;z-index:60;width:3.75rem;height:3.75rem;border-radius:999px;padding:0;border:2px solid color-mix(in oklab, var(--color-primary) 60%, transparent);background:var(--color-base-100);cursor:pointer;overflow:hidden;box-shadow:0 0 22px color-mix(in oklab, var(--color-primary) 45%, transparent);transition:transform 0.15s ease;}.fab.svelte-13e87sq:hover {transform:scale(1.06);}.fab.hidden.svelte-13e87sq {display:none;}.fab.svelte-13e87sq img:where(.svelte-13e87sq) {width:100%;height:100%;object-fit:cover;}.panel.svelte-13e87sq {position:fixed;z-index:61;display:flex;flex-direction:column;background:var(--color-base-100);border:1px solid color-mix(in oklab, var(--color-primary) 30%, transparent);box-shadow:0 0 32px color-mix(in oklab, var(--color-primary) 30%, transparent);overflow:hidden;}.panel.floating.svelte-13e87sq {right:1.5rem;bottom:1.5rem;width:22.5rem;height:32rem;max-width:calc(100vw - 2rem);max-height:calc(100vh - 2rem);border-radius:1.25rem;}\r\n\r\n    /* Docked, full-height sidebar (expand). */.panel.sidebar.svelte-13e87sq {top:0;right:0;bottom:0;width:min(28rem, 100vw);height:100vh;border-radius:0;border:none;border-left:1px solid color-mix(in oklab, var(--color-primary) 30%, transparent);}.panel-header.svelte-13e87sq {flex:0 0 auto;display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:0.75rem 1rem;border-bottom:1px solid color-mix(in oklab, var(--color-base-content) 10%, transparent);}.panel.floating.svelte-13e87sq .panel-header:where(.svelte-13e87sq) {cursor:grab;}.panel.floating.svelte-13e87sq .panel-header:where(.svelte-13e87sq):active {cursor:grabbing;}.panel-title.svelte-13e87sq {font-weight:700;letter-spacing:0.03em;color:var(--color-base-content);}.panel-actions.svelte-13e87sq {display:flex;gap:0.35rem;}.icon-btn.svelte-13e87sq {display:grid;place-items:center;width:1.75rem;height:1.75rem;border-radius:0.5rem;border:none;background:transparent;color:color-mix(in oklab, var(--color-base-content) 70%, transparent);cursor:pointer;}.icon-btn.svelte-13e87sq:hover {background:color-mix(in oklab, var(--color-base-content) 10%, transparent);color:var(--color-base-content);}.panel-body.svelte-13e87sq {flex:1;min-height:0;overflow-y:auto;padding:1rem;display:flex;flex-direction:column;gap:0.75rem;}.message.svelte-13e87sq {display:flex;align-items:flex-start;gap:0.6rem;}.message.user.svelte-13e87sq {justify-content:flex-end;}.avatar.svelte-13e87sq {width:2.25rem;height:2.25rem;flex:0 0 auto;border-radius:999px;object-fit:cover;}.bubble.svelte-13e87sq {padding:0.75rem 0.9rem;border-radius:0.9rem;border-top-left-radius:0.25rem;line-height:1.5;color:var(--color-base-content);background:color-mix(in oklab, var(--color-primary) 12%, transparent);border:1px solid color-mix(in oklab, var(--color-primary) 28%, transparent);}.composer.svelte-13e87sq {flex:0 0 auto;display:flex;flex-direction:column;gap:0.4rem;padding:0.75rem;border-top:1px solid color-mix(in oklab, var(--color-base-content) 10%, transparent);}.coming-soon.svelte-13e87sq {align-self:center;font-size:0.7rem;color:var(--color-warning);}.composer-row.svelte-13e87sq {display:flex;align-items:center;gap:0.5rem;padding:0.35rem 0.5rem;border-radius:999px;background:color-mix(in oklab, var(--color-base-200) 80%, transparent);border:1px solid color-mix(in oklab, var(--color-primary) 30%, transparent);}.composer-add.svelte-13e87sq,\r\n    .composer-send.svelte-13e87sq {display:grid;place-items:center;width:1.9rem;height:1.9rem;flex:0 0 auto;border-radius:999px;border:none;cursor:not-allowed;color:var(--color-primary-content);background:color-mix(in oklab, var(--color-primary) 70%, transparent);}.composer-input.svelte-13e87sq {flex:1 1 auto;background:transparent;border:none;color:var(--color-base-content);padding:0.25rem;}.composer-input.svelte-13e87sq:focus {outline:none;}.disclaimer.svelte-13e87sq {text-align:center;font-size:0.65rem;color:color-mix(in oklab, var(--color-base-content) 55%, transparent);}"
};
function ChatWidget($$anchor, $$props) {
  push($$props, true);
  append_styles($$anchor, $$css2);
  let onSidebarChange = prop($$props, "onSidebarChange", 7);
  let open = state(false);
  let mode = state("floating");
  let pos = state(null);
  let dragOffset = null;
  const chat = createAiChatStore();
  let chatState = state(proxy({ connection: "disconnected", errorMessage: "", messages: [] }));
  let draft = state("");
  let connectStarted = false;
  const connected = user_derived(() => get2(chatState).connection === "connected");
  function ensureConnected() {
    if (!connectStarted) {
      connectStarted = true;
      void chat.connect();
    }
  }
  async function send() {
    const text2 = get2(draft).trim();
    if (!text2 || !get2(connected)) {
      return;
    }
    set(draft, "");
    await chat.sendChatInput("markdown", text2);
  }
  function notify() {
    onSidebarChange()?.(get2(open) && get2(mode) === "sidebar");
  }
  onMount(() => {
    notify();
    const unsubscribe = chat.subscribe((value) => {
      set(chatState, value, true);
    });
    return () => {
      unsubscribe();
      void chat.disconnect();
    };
  });
  function toggle() {
    set(open, !get2(open));
    if (get2(open)) {
      ensureConnected();
    }
    notify();
  }
  function close() {
    set(open, false);
    notify();
  }
  function toggleMode() {
    set(mode, get2(mode) === "floating" ? "sidebar" : "floating", true);
    set(pos, null);
    notify();
  }
  function onPointerMove(event2) {
    if (!dragOffset) {
      return;
    }
    const maxX = Math.max(0, window.innerWidth - 360);
    const maxY = Math.max(0, window.innerHeight - 120);
    set(
      pos,
      {
        x: Math.min(Math.max(0, event2.clientX - dragOffset.x), maxX),
        y: Math.min(Math.max(0, event2.clientY - dragOffset.y), maxY)
      },
      true
    );
  }
  function onPointerUp() {
    dragOffset = null;
    window.removeEventListener("pointermove", onPointerMove);
    window.removeEventListener("pointerup", onPointerUp);
  }
  function startDrag(event2) {
    if (get2(mode) !== "floating") {
      return;
    }
    const panel = event2.currentTarget.parentElement;
    if (!panel) {
      return;
    }
    const rect = panel.getBoundingClientRect();
    dragOffset = { x: event2.clientX - rect.left, y: event2.clientY - rect.top };
    set(pos, { x: rect.left, y: rect.top }, true);
    window.addEventListener("pointermove", onPointerMove);
    window.addEventListener("pointerup", onPointerUp);
  }
  var $$exports = {
    get onSidebarChange() {
      return onSidebarChange();
    },
    set onSidebarChange($$value) {
      onSidebarChange($$value);
      flushSync();
    }
  };
  var fragment = root_4();
  var node = first_child(fragment);
  {
    var consequent_2 = ($$anchor2) => {
      var section = root_3();
      let classes;
      var header = child(section);
      var span = child(header);
      var text_1 = child(span, true);
      reset(span);
      var div = sibling(span, 2);
      var button = child(div);
      var text_2 = child(button, true);
      reset(button);
      var button_1 = sibling(button, 2);
      reset(div);
      reset(header);
      var div_1 = sibling(header, 2);
      var node_1 = sibling(child(div_1), 2);
      each(node_1, 17, () => get2(chatState).messages, (message) => message.id, ($$anchor3, message) => {
        var div_2 = root_12();
        let classes_1;
        var node_2 = child(div_2);
        {
          var consequent = ($$anchor4) => {
            var img = root2();
            append($$anchor4, img);
          };
          if_block(node_2, ($$render) => {
            if (get2(message).sender === "assistant") $$render(consequent);
          });
        }
        var div_3 = sibling(node_2, 2);
        let classes_2;
        var text_3 = child(div_3, true);
        reset(div_3);
        reset(div_2);
        template_effect(() => {
          classes_1 = set_class(div_2, 1, "message svelte-13e87sq", null, classes_1, { user: get2(message).sender === "user" });
          classes_2 = set_class(div_3, 1, "bubble svelte-13e87sq", null, classes_2, { user: get2(message).sender === "user" });
          set_text(text_3, get2(message).content);
        });
        append($$anchor3, div_2);
      });
      reset(div_1);
      var div_4 = sibling(div_1, 2);
      var node_3 = child(div_4);
      {
        var consequent_1 = ($$anchor3) => {
          var span_1 = root_2();
          var text_4 = child(span_1, true);
          reset(span_1);
          template_effect(() => set_text(text_4, get2(chatState).connection === "connecting" ? "Connecting\u2026" : "Offline \u2014 reconnecting\u2026"));
          append($$anchor3, span_1);
        };
        if_block(node_3, ($$render) => {
          if (!get2(connected)) $$render(consequent_1);
        });
      }
      var form = sibling(node_3, 2);
      var input = sibling(child(form), 2);
      remove_input_defaults(input);
      var button_2 = sibling(input, 2);
      reset(form);
      next(2);
      reset(div_4);
      reset(section);
      template_effect(
        ($0) => {
          classes = set_class(section, 1, "panel svelte-13e87sq", null, classes, {
            floating: get2(mode) === "floating",
            sidebar: get2(mode) === "sidebar"
          });
          set_style(section, get2(mode) === "floating" && get2(pos) ? `left:${get2(pos).x}px; top:${get2(pos).y}px; right:auto; bottom:auto;` : "");
          set_text(text_1, get2(mode) === "sidebar" ? "Quiz Chat" : "Quick Chat");
          set_attribute2(button, "aria-label", get2(mode) === "sidebar" ? "Float chat" : "Dock chat to sidebar");
          set_text(text_2, get2(mode) === "sidebar" ? "\u2199" : "\u2197");
          input.disabled = !get2(connected);
          button_2.disabled = $0;
        },
        [() => !get2(connected) || get2(draft).trim().length === 0]
      );
      delegated("pointerdown", header, startDrag);
      delegated("click", button, toggleMode);
      delegated("click", button_1, close);
      event("submit", form, (event2) => {
        event2.preventDefault();
        send();
      });
      bind_value(input, () => get2(draft), ($$value) => set(draft, $$value));
      append($$anchor2, section);
    };
    if_block(node, ($$render) => {
      if (get2(open)) $$render(consequent_2);
    });
  }
  var button_3 = sibling(node, 2);
  let classes_3;
  template_effect(() => classes_3 = set_class(button_3, 1, "fab svelte-13e87sq", null, classes_3, { hidden: get2(open) }));
  delegated("click", button_3, toggle);
  append($$anchor, fragment);
  return pop($$exports);
}
delegate(["pointerdown", "click"]);
create_custom_element(ChatWidget, { onSidebarChange: {} }, [], [], { mode: "open" });

// src/components/basic/ProgressBar.svelte
var root3 = from_html(`<div class="progress-track svelte-sbeapt" role="progressbar"><div class="progress-fill svelte-sbeapt"></div></div>`);
var $$css3 = {
  hash: "svelte-sbeapt",
  code: ".progress-track.svelte-sbeapt {height:0.9rem;border-radius:999px;overflow:hidden;background:color-mix(in oklab, var(--color-base-content) 12%, transparent);}.progress-fill.svelte-sbeapt {height:100%;border-radius:999px;background:linear-gradient(90deg, var(--color-warning), var(--color-success));box-shadow:0 0 12px color-mix(in oklab, var(--color-success) 45%, transparent);transition:width 0.3s ease;}"
};
function ProgressBar($$anchor, $$props) {
  push($$props, true);
  append_styles($$anchor, $$css3);
  "use strict";
  let value = prop($$props, "value", 7), label = prop($$props, "label", 7, "");
  const percent = user_derived(() => Math.min(100, Math.max(0, value())));
  var $$exports = {
    get value() {
      return value();
    },
    set value($$value) {
      value($$value);
      flushSync();
    },
    get label() {
      return label();
    },
    set label($$value = "") {
      label($$value);
      flushSync();
    }
  };
  var div = root3();
  set_attribute2(div, "aria-valuemin", 0);
  set_attribute2(div, "aria-valuemax", 100);
  var div_1 = child(div);
  reset(div);
  template_effect(
    ($0) => {
      set_attribute2(div, "aria-valuenow", $0);
      set_attribute2(div, "aria-label", label());
      set_style(div_1, `width: ${get2(percent) ?? ""}%`);
    },
    [() => Math.round(get2(percent))]
  );
  append($$anchor, div);
  return pop($$exports);
}
create_custom_element(ProgressBar, { value: {}, label: {} }, [], [], { mode: "open" });

// src/components/basic/SegmentedTabs.svelte
var root4 = from_html(`<button type="button" role="tab"> </button>`);
var root_13 = from_html(`<div role="tablist" class="seg-tabs svelte-1rwwumd" aria-label="Learning views"></div>`);
var $$css4 = {
  hash: "svelte-1rwwumd",
  code: ".seg-tabs.svelte-1rwwumd {display:inline-flex;gap:0.25rem;}.seg-tab.svelte-1rwwumd {padding:0.25rem 0.75rem;border-radius:0.5rem;font-size:0.85rem;font-weight:600;letter-spacing:0.04em;color:color-mix(in oklab, var(--color-base-content) 65%, transparent);background:transparent;cursor:pointer;}.seg-tab.svelte-1rwwumd:hover:not(:disabled) {color:var(--color-base-content);}.seg-tab.active.svelte-1rwwumd {color:var(--color-primary);background:color-mix(in oklab, var(--color-primary) 16%, transparent);}.seg-tab.svelte-1rwwumd:disabled {cursor:not-allowed;opacity:0.45;}.seg-tab.svelte-1rwwumd:focus-visible {outline:2px solid var(--color-primary);outline-offset:2px;}"
};
function SegmentedTabs($$anchor, $$props) {
  push($$props, true);
  append_styles($$anchor, $$css4);
  "use strict";
  let tabs = prop($$props, "tabs", 7), active = prop($$props, "active", 7), disabledTabs = prop($$props, "disabledTabs", 23, () => []), onSelect = prop($$props, "onSelect", 7);
  var $$exports = {
    get tabs() {
      return tabs();
    },
    set tabs($$value) {
      tabs($$value);
      flushSync();
    },
    get active() {
      return active();
    },
    set active($$value) {
      active($$value);
      flushSync();
    },
    get disabledTabs() {
      return disabledTabs();
    },
    set disabledTabs($$value = []) {
      disabledTabs($$value);
      flushSync();
    },
    get onSelect() {
      return onSelect();
    },
    set onSelect($$value) {
      onSelect($$value);
      flushSync();
    }
  };
  var div = root_13();
  each(div, 20, tabs, (tab) => tab, ($$anchor2, tab) => {
    var button = root4();
    let classes;
    var text2 = child(button, true);
    reset(button);
    template_effect(
      ($0) => {
        classes = set_class(button, 1, "seg-tab svelte-1rwwumd", null, classes, { active: tab === active() });
        set_attribute2(button, "aria-selected", tab === active());
        button.disabled = $0;
        set_text(text2, tab);
      },
      [() => disabledTabs().includes(tab)]
    );
    delegated("click", button, () => onSelect()?.(tab));
    append($$anchor2, button);
  });
  reset(div);
  append($$anchor, div);
  return pop($$exports);
}
delegate(["click"]);
create_custom_element(SegmentedTabs, { tabs: {}, active: {}, disabledTabs: {}, onSelect: {} }, [], [], { mode: "open" });

// src/components/panels/MyLearningPanel.svelte
var root5 = from_html(`<p class="empty svelte-q1lzti">No courses in progress yet. Enrol in a course to see it here.</p>`);
var root_14 = from_html(`<span class="tag svelte-q1lzti"> </span>`);
var root_22 = from_html(`<button type="button" class="course-card svelte-q1lzti"><div class="course-head svelte-q1lzti"><span class="course-name svelte-q1lzti"> </span> <span class="course-bar svelte-q1lzti"><!></span> <span class="course-percent svelte-q1lzti"> </span> <span class="course-go svelte-q1lzti" aria-hidden="true">\u203A</span></div> <div class="course-tags svelte-q1lzti"></div></button>`);
var root_32 = from_html(`<div class="path-step svelte-q1lzti"><span class="step-num svelte-q1lzti"> </span> <span class="step-title svelte-q1lzti"> </span> <span class="step-status svelte-q1lzti"> </span></div>`);
var root_42 = from_html(`<div class="repeat-item svelte-q1lzti"><span class="repeat-title svelte-q1lzti"> </span> <span class="repeat-due svelte-q1lzti"> </span></div>`);
var root_5 = from_html(`<div class="locked svelte-q1lzti"><div class="locked-content svelte-q1lzti" aria-hidden="true"><!></div> <div class="locked-overlay svelte-q1lzti" role="status"><span class="overlay-badge svelte-q1lzti">\u{1F6A7} Coming soon</span> <span class="overlay-note svelte-q1lzti"> </span></div></div>`);
var root_6 = from_html(`<section class="card panel svelte-q1lzti"><header class="panel-head svelte-q1lzti"><h2 class="panel-title svelte-q1lzti">My Learning</h2> <!></header> <div class="panel-body svelte-q1lzti"><!></div></section>`);
var $$css5 = {
  hash: "svelte-q1lzti",
  code: '\r\n    /* Fill the grid cell at a fixed height; the body scrolls instead of growing. */.panel.svelte-q1lzti {flex:1;min-height:0;display:flex;flex-direction:column;background:var(--color-base-100);border-radius:1.25rem;padding:1.75rem;box-shadow:0 0 24px color-mix(in oklab, var(--color-primary) 10%, transparent);}.panel-head.svelte-q1lzti {flex:0 0 auto;display:flex;align-items:center;justify-content:space-between;gap:1rem;padding-bottom:1rem;margin-bottom:0.5rem;border-bottom:1px solid color-mix(in oklab, var(--color-base-content) 8%, transparent);}.panel-title.svelte-q1lzti {font-size:1.5rem;font-weight:700;letter-spacing:0.02em;color:var(--color-base-content);}\r\n\r\n    /* Scroll area: keeps the card a fixed size regardless of how many courses. */.panel-body.svelte-q1lzti {flex:1;min-height:0;overflow-y:auto;padding-right:0.5rem;display:flex;flex-direction:column;gap:0.75rem;}.panel-body.svelte-q1lzti::-webkit-scrollbar {width:0.5rem;}.panel-body.svelte-q1lzti::-webkit-scrollbar-thumb {border-radius:999px;background:color-mix(in oklab, var(--color-base-content) 20%, transparent);}\r\n\r\n    /* A whole course is one clickable card. */.course-card.svelte-q1lzti {display:block;width:100%;text-align:left;cursor:pointer;background:color-mix(in oklab, var(--color-base-200) 50%, transparent);border:1px solid color-mix(in oklab, var(--color-base-content) 8%, transparent);border-radius:1rem;padding:1rem 1.25rem;transition:border-color 0.2s ease, background 0.2s ease;}.course-card.svelte-q1lzti:hover {background:color-mix(in oklab, var(--color-primary) 12%, transparent);border-color:color-mix(in oklab, var(--color-primary) 45%, transparent);}.course-card.svelte-q1lzti:focus-visible {outline:2px solid var(--color-primary);outline-offset:2px;}\r\n\r\n    /* Fixed name + percent columns => the 1fr bar column is identical on every row. */.course-head.svelte-q1lzti {display:grid;grid-template-columns:14rem 1fr 3.5rem auto;align-items:center;gap:1rem;}.course-name.svelte-q1lzti {font-size:1.6rem;font-weight:700;color:var(--color-base-content);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}.course-bar.svelte-q1lzti {min-width:0;}.course-percent.svelte-q1lzti {font-weight:700;text-align:right;color:var(--color-base-content);}.course-go.svelte-q1lzti {display:grid;place-items:center;width:2rem;height:2rem;border-radius:999px;font-size:1.2rem;line-height:1;color:var(--color-primary-content);background:var(--color-primary);box-shadow:0 0 12px color-mix(in oklab, var(--color-primary) 45%, transparent);}.course-tags.svelte-q1lzti {display:flex;flex-wrap:wrap;gap:0.4rem;margin-top:0.75rem;}.tag.svelte-q1lzti {font-size:0.75rem;padding:0.15rem 0.6rem;border-radius:999px;color:color-mix(in oklab, var(--color-base-content) 75%, transparent);background:color-mix(in oklab, var(--color-base-content) 10%, transparent);border:1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);}.empty.svelte-q1lzti {color:color-mix(in oklab, var(--color-base-content) 60%, transparent);padding:1.5rem 0;}\r\n\r\n    /* Mock content for Path/Repeat, blurred behind a "Coming soon" overlay. */.locked.svelte-q1lzti {position:relative;flex:1;min-height:0;}.locked-content.svelte-q1lzti {display:flex;flex-direction:column;gap:0.75rem;filter:blur(5px);opacity:0.5;pointer-events:none;user-select:none;}.locked-overlay.svelte-q1lzti {position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0.5rem;text-align:center;}.overlay-badge.svelte-q1lzti {padding:0.4rem 1rem;border-radius:999px;font-weight:700;letter-spacing:0.04em;color:var(--color-warning);background:color-mix(in oklab, var(--color-warning) 16%, transparent);border:1px solid color-mix(in oklab, var(--color-warning) 40%, transparent);}.overlay-note.svelte-q1lzti {font-size:0.85rem;color:color-mix(in oklab, var(--color-base-content) 70%, transparent);}.path-step.svelte-q1lzti,\r\n    .repeat-item.svelte-q1lzti {display:flex;align-items:center;gap:1rem;padding:0.9rem 1.1rem;border-radius:1rem;background:color-mix(in oklab, var(--color-base-200) 50%, transparent);border:1px solid color-mix(in oklab, var(--color-base-content) 8%, transparent);}.repeat-item.svelte-q1lzti {justify-content:space-between;}.step-num.svelte-q1lzti {display:grid;place-items:center;width:2rem;height:2rem;flex:0 0 auto;border-radius:999px;font-weight:700;color:var(--color-primary-content);background:var(--color-primary);}.step-title.svelte-q1lzti,\r\n    .repeat-title.svelte-q1lzti {flex:1 1 auto;font-weight:600;color:var(--color-base-content);}.step-status.svelte-q1lzti {font-size:0.8rem;color:color-mix(in oklab, var(--color-base-content) 65%, transparent);}.repeat-due.svelte-q1lzti {flex:0 0 auto;font-size:0.8rem;padding:0.15rem 0.6rem;border-radius:999px;color:var(--color-primary);background:color-mix(in oklab, var(--color-primary) 14%, transparent);}'
};
function MyLearningPanel($$anchor, $$props) {
  push($$props, true);
  append_styles($$anchor, $$css5);
  let courses = prop($$props, "courses", 7), skills = prop($$props, "skills", 7), onCourseOpen = prop($$props, "onCourseOpen", 7);
  const tabs = ["Current", "Path", "Repeat"];
  let activeTab = state("Current");
  const isEmpty = user_derived(() => courses().length === 0);
  const pathSteps = [
    { step: 1, title: "Foundations", status: "Completed" },
    { step: 2, title: "Core concepts", status: "In progress" },
    { step: 3, title: "Hands-on practice", status: "Locked" },
    { step: 4, title: "Mastery project", status: "Locked" }
  ];
  const repeatItems = [
    { title: "HTML structure", due: "Due today" },
    { title: "CSS selectors", due: "Due in 2 days" },
    { title: "JS functions", due: "New" }
  ];
  const fallbackPool = [
    "Grundlagen",
    "HTML",
    "CSS",
    "JavaScript",
    "SQL",
    "Datenmodellierung"
  ];
  const tagPool = user_derived(() => skills().length > 0 ? skills().map((skill) => skill.name) : fallbackPool);
  function courseTags(index2) {
    const pool = get2(tagPool);
    if (pool.length === 0) {
      return [];
    }
    const count = Math.min(3, pool.length);
    return Array.from({ length: count }, (_, offset) => pool[(index2 + offset) % pool.length]);
  }
  var $$exports = {
    get courses() {
      return courses();
    },
    set courses($$value) {
      courses($$value);
      flushSync();
    },
    get skills() {
      return skills();
    },
    set skills($$value) {
      skills($$value);
      flushSync();
    },
    get onCourseOpen() {
      return onCourseOpen();
    },
    set onCourseOpen($$value) {
      onCourseOpen($$value);
      flushSync();
    }
  };
  var section = root_6();
  var header = child(section);
  var node = sibling(child(header), 2);
  SegmentedTabs(node, {
    get tabs() {
      return tabs;
    },
    get active() {
      return get2(activeTab);
    },
    onSelect: (tab) => set(activeTab, tab, true)
  });
  reset(header);
  var div = sibling(header, 2);
  var node_1 = child(div);
  {
    var consequent_1 = ($$anchor2) => {
      var fragment = comment();
      var node_2 = first_child(fragment);
      {
        var consequent = ($$anchor3) => {
          var p = root5();
          append($$anchor3, p);
        };
        var alternate = ($$anchor3) => {
          var fragment_1 = comment();
          var node_3 = first_child(fragment_1);
          each(node_3, 19, courses, (course) => course.id, ($$anchor4, course, index2) => {
            var button = root_22();
            var div_1 = child(button);
            var span = child(div_1);
            var text2 = child(span, true);
            reset(span);
            var span_1 = sibling(span, 2);
            var node_4 = child(span_1);
            {
              let $0 = user_derived(() => `${get2(course).name} progress`);
              ProgressBar(node_4, {
                get value() {
                  return get2(course).progress;
                },
                get label() {
                  return get2($0);
                }
              });
            }
            reset(span_1);
            var span_2 = sibling(span_1, 2);
            var text_1 = child(span_2);
            reset(span_2);
            next(2);
            reset(div_1);
            var div_2 = sibling(div_1, 2);
            each(div_2, 20, () => courseTags(get2(index2)), (tag2) => tag2, ($$anchor5, tag2) => {
              var span_3 = root_14();
              var text_2 = child(span_3, true);
              reset(span_3);
              template_effect(() => set_text(text_2, tag2));
              append($$anchor5, span_3);
            });
            reset(div_2);
            reset(button);
            template_effect(
              ($0) => {
                set_text(text2, get2(course).name);
                set_text(text_1, `${$0 ?? ""}%`);
              },
              [() => Math.round(get2(course).progress)]
            );
            delegated("click", button, () => onCourseOpen()?.(get2(course)));
            append($$anchor4, button);
          });
          append($$anchor3, fragment_1);
        };
        if_block(node_2, ($$render) => {
          if (get2(isEmpty)) $$render(consequent);
          else $$render(alternate, -1);
        });
      }
      append($$anchor2, fragment);
    };
    var alternate_2 = ($$anchor2) => {
      var div_3 = root_5();
      var div_4 = child(div_3);
      var node_5 = child(div_4);
      {
        var consequent_2 = ($$anchor3) => {
          var fragment_2 = comment();
          var node_6 = first_child(fragment_2);
          each(node_6, 17, () => pathSteps, (item) => item.step, ($$anchor4, item) => {
            var div_5 = root_32();
            var span_4 = child(div_5);
            var text_3 = child(span_4, true);
            reset(span_4);
            var span_5 = sibling(span_4, 2);
            var text_4 = child(span_5, true);
            reset(span_5);
            var span_6 = sibling(span_5, 2);
            var text_5 = child(span_6, true);
            reset(span_6);
            reset(div_5);
            template_effect(() => {
              set_text(text_3, get2(item).step);
              set_text(text_4, get2(item).title);
              set_text(text_5, get2(item).status);
            });
            append($$anchor4, div_5);
          });
          append($$anchor3, fragment_2);
        };
        var alternate_1 = ($$anchor3) => {
          var fragment_3 = comment();
          var node_7 = first_child(fragment_3);
          each(node_7, 17, () => repeatItems, (item) => item.title, ($$anchor4, item) => {
            var div_6 = root_42();
            var span_7 = child(div_6);
            var text_6 = child(span_7, true);
            reset(span_7);
            var span_8 = sibling(span_7, 2);
            var text_7 = child(span_8, true);
            reset(span_8);
            reset(div_6);
            template_effect(() => {
              set_text(text_6, get2(item).title);
              set_text(text_7, get2(item).due);
            });
            append($$anchor4, div_6);
          });
          append($$anchor3, fragment_3);
        };
        if_block(node_5, ($$render) => {
          if (get2(activeTab) === "Path") $$render(consequent_2);
          else $$render(alternate_1, -1);
        });
      }
      reset(div_4);
      var div_7 = sibling(div_4, 2);
      var span_9 = sibling(child(div_7), 2);
      var text_8 = child(span_9);
      reset(span_9);
      reset(div_7);
      reset(div_3);
      template_effect(() => set_text(text_8, `${get2(activeTab) ?? ""} mode is in the works.`));
      append($$anchor2, div_3);
    };
    if_block(node_1, ($$render) => {
      if (get2(activeTab) === "Current") $$render(consequent_1);
      else $$render(alternate_2, -1);
    });
  }
  reset(div);
  reset(section);
  append($$anchor, section);
  return pop($$exports);
}
delegate(["click"]);
create_custom_element(MyLearningPanel, { courses: {}, skills: {}, onCourseOpen: {} }, [], [], { mode: "open" });

// src/components/basic/StatTile.svelte
var root6 = from_html(`<div class="stat-tile svelte-de708j"><span class="stat-icon svelte-de708j" aria-hidden="true"> </span> <span class="stat-value svelte-de708j"> </span> <span class="sr-only svelte-de708j"> </span></div>`);
var $$css6 = {
  hash: "svelte-de708j",
  code: ".stat-tile.svelte-de708j {display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0.35rem;text-align:center;}.stat-icon.svelte-de708j {display:block;width:100%;text-align:center;font-size:1.5rem;line-height:1;}.stat-value.svelte-de708j {display:block;width:100%;text-align:center;font-weight:700;font-size:1.1rem;color:var(--color-base-content);}.sr-only.svelte-de708j {position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0, 0, 0, 0);white-space:nowrap;border:0;}"
};
function StatTile($$anchor, $$props) {
  push($$props, true);
  append_styles($$anchor, $$css6);
  "use strict";
  let icon = prop($$props, "icon", 7), value = prop($$props, "value", 7), label = prop($$props, "label", 7);
  var $$exports = {
    get icon() {
      return icon();
    },
    set icon($$value) {
      icon($$value);
      flushSync();
    },
    get value() {
      return value();
    },
    set value($$value) {
      value($$value);
      flushSync();
    },
    get label() {
      return label();
    },
    set label($$value) {
      label($$value);
      flushSync();
    }
  };
  var div = root6();
  var span = child(div);
  var text2 = child(span, true);
  reset(span);
  var span_1 = sibling(span, 2);
  var text_1 = child(span_1, true);
  reset(span_1);
  var span_2 = sibling(span_1, 2);
  var text_2 = child(span_2, true);
  reset(span_2);
  reset(div);
  template_effect(() => {
    set_attribute2(div, "title", label());
    set_text(text2, icon());
    set_text(text_1, value());
    set_text(text_2, label());
  });
  append($$anchor, div);
  return pop($$exports);
}
create_custom_element(StatTile, { icon: {}, value: {}, label: {} }, [], [], { mode: "open" });

// src/components/panels/StatsPanel.svelte
var root7 = from_html(`<img alt="" class="svelte-1tag4vz"/>`);
var root_15 = from_html(`<section class="card panel svelte-1tag4vz"><header class="panel-head svelte-1tag4vz"><h2 class="panel-title svelte-1tag4vz">My Stats</h2> <button type="button" class="btn btn-outline btn-sm">Go to Profile</button></header> <div class="identity svelte-1tag4vz"><span class="avatar-mark svelte-1tag4vz" aria-hidden="true"><!></span> <div class="identity-text svelte-1tag4vz"><span class="username svelte-1tag4vz"> </span> <div class="level-row svelte-1tag4vz"><span class="level-label svelte-1tag4vz"> </span> <div class="level-bar svelte-1tag4vz"><!></div> <span class="level-points svelte-1tag4vz"> </span></div></div></div> <div class="stat-grid svelte-1tag4vz"><!> <!> <!> <!></div></section>`);
var $$css7 = {
  hash: "svelte-1tag4vz",
  code: ".panel.svelte-1tag4vz {background:var(--color-base-100);border-radius:1rem;padding:1.5rem;box-shadow:0 0 24px color-mix(in oklab, var(--color-primary) 10%, transparent);}.panel-head.svelte-1tag4vz {display:flex;align-items:center;justify-content:space-between;gap:1rem;margin-bottom:1.25rem;}.panel-title.svelte-1tag4vz {font-size:1.3rem;font-weight:700;color:var(--color-base-content);}.identity.svelte-1tag4vz {display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem;}.avatar-mark.svelte-1tag4vz {width:3.5rem;height:3.5rem;flex:0 0 auto;border-radius:999px;overflow:hidden;background:color-mix(in oklab, var(--color-base-content) 18%, transparent);box-shadow:0 0 16px color-mix(in oklab, var(--color-primary) 35%, transparent);}.avatar-mark.svelte-1tag4vz img:where(.svelte-1tag4vz) {width:100%;height:100%;object-fit:cover;}.identity-text.svelte-1tag4vz {flex:1 1 auto;min-width:0;}.username.svelte-1tag4vz {display:block;font-size:1.1rem;font-weight:600;color:var(--color-base-content);}.level-row.svelte-1tag4vz {display:flex;align-items:center;gap:0.6rem;margin-top:0.35rem;}.level-label.svelte-1tag4vz {font-size:0.8rem;white-space:nowrap;color:color-mix(in oklab, var(--color-base-content) 70%, transparent);}.level-bar.svelte-1tag4vz {flex:1 1 auto;}.level-points.svelte-1tag4vz {font-weight:700;color:var(--color-base-content);}.stat-grid.svelte-1tag4vz {display:grid;grid-template-columns:repeat(4, 1fr);gap:0.75rem;}"
};
function StatsPanel($$anchor, $$props) {
  push($$props, true);
  append_styles($$anchor, $$css7);
  let user = prop($$props, "user", 7), stats = prop($$props, "stats", 7), onProfile = prop($$props, "onProfile", 7);
  const numberFormat = new Intl.NumberFormat();
  const username = user_derived(() => user()?.username ?? "user");
  const points = user_derived(() => stats()?.points ?? 0);
  const level = user_derived(() => stats()?.level ?? 1);
  const levelProgress2 = user_derived(() => stats()?.levelProgress ?? 0);
  const nextLevelPoints = user_derived(() => stats()?.nextLevelPoints ?? get2(points));
  function format(value) {
    return numberFormat.format(value);
  }
  var $$exports = {
    get user() {
      return user();
    },
    set user($$value) {
      user($$value);
      flushSync();
    },
    get stats() {
      return stats();
    },
    set stats($$value) {
      stats($$value);
      flushSync();
    },
    get onProfile() {
      return onProfile();
    },
    set onProfile($$value) {
      onProfile($$value);
      flushSync();
    }
  };
  var section = root_15();
  var header = child(section);
  var button = sibling(child(header), 2);
  reset(header);
  var div = sibling(header, 2);
  var span = child(div);
  var node = child(span);
  {
    var consequent = ($$anchor2) => {
      var img = root7();
      template_effect(() => set_attribute2(img, "src", user().avatarUrl));
      append($$anchor2, img);
    };
    if_block(node, ($$render) => {
      if (user()?.avatarUrl) $$render(consequent);
    });
  }
  reset(span);
  var div_1 = sibling(span, 2);
  var span_1 = child(div_1);
  var text2 = child(span_1, true);
  reset(span_1);
  var div_2 = sibling(span_1, 2);
  var span_2 = child(div_2);
  var text_1 = child(span_2);
  reset(span_2);
  var div_3 = sibling(span_2, 2);
  var node_1 = child(div_3);
  {
    let $0 = user_derived(() => `Level ${get2(level)} progress`);
    ProgressBar(node_1, {
      get value() {
        return get2(levelProgress2);
      },
      get label() {
        return get2($0);
      }
    });
  }
  reset(div_3);
  var span_3 = sibling(div_3, 2);
  var text_2 = child(span_3, true);
  reset(span_3);
  reset(div_2);
  reset(div_1);
  reset(div);
  var div_4 = sibling(div, 2);
  var node_2 = child(div_4);
  {
    let $0 = user_derived(() => format(stats()?.currentStreak ?? 0));
    StatTile(node_2, {
      icon: "\u{1F525}",
      get value() {
        return get2($0);
      },
      label: "Current streak"
    });
  }
  var node_3 = sibling(node_2, 2);
  {
    let $0 = user_derived(() => format(stats()?.longestStreak ?? 0));
    StatTile(node_3, {
      icon: "\u{1F3C6}",
      get value() {
        return get2($0);
      },
      label: "Longest streak"
    });
  }
  var node_4 = sibling(node_3, 2);
  {
    let $0 = user_derived(() => format(get2(points)));
    StatTile(node_4, {
      icon: "\u{1F3AF}",
      get value() {
        return get2($0);
      },
      label: "Total points"
    });
  }
  var node_5 = sibling(node_4, 2);
  {
    let $0 = user_derived(() => format(get2(level)));
    StatTile(node_5, {
      icon: "\u{1F3C5}",
      get value() {
        return get2($0);
      },
      label: "Level"
    });
  }
  reset(div_4);
  reset(section);
  template_effect(
    ($0) => {
      set_text(text2, get2(username));
      set_text(text_1, `Level ${get2(level) ?? ""}`);
      set_text(text_2, $0);
    },
    [() => format(get2(nextLevelPoints))]
  );
  delegated("click", button, () => onProfile()?.());
  append($$anchor, section);
  return pop($$exports);
}
delegate(["click"]);
create_custom_element(StatsPanel, { user: {}, stats: {}, onProfile: {} }, [], [], { mode: "open" });

// src/components/panels/SkillMatrixPanel.svelte
var root8 = from_html(`<p class="empty svelte-168eojm">No skills yet. Complete tasks and quizzes in your courses to earn skills.</p>`);
var root_16 = from_html(`<div class="skill-row svelte-168eojm"><div class="skill-head svelte-168eojm"><span class="skill-name svelte-168eojm"> </span> <span class="skill-level svelte-168eojm"> </span></div> <div class="skill-bar svelte-168eojm"><!> <span class="skill-percent svelte-168eojm"> </span></div></div>`);
var root_23 = from_html(`<section class="card panel svelte-168eojm"><h2 class="panel-title svelte-168eojm">Skills</h2> <div class="panel-body svelte-168eojm"><!></div></section>`);
var $$css8 = {
  hash: "svelte-168eojm",
  code: '\n    /* Fill the remaining height of the right column; the body scrolls if needed. */.panel.svelte-168eojm {flex:1;min-height:0;display:flex;flex-direction:column;background:var(--color-base-100);border-radius:1.25rem;padding:1.75rem;box-shadow:0 0 24px color-mix(in oklab, var(--color-primary) 10%, transparent);}.panel-title.svelte-168eojm {flex:0 0 auto;font-size:1.5rem;font-weight:700;margin-bottom:1rem;color:var(--color-base-content);}.panel-body.svelte-168eojm {flex:1;min-height:0;overflow-y:auto;padding-right:0.5rem;display:flex;flex-direction:column;gap:0.75rem;}.panel-body.svelte-168eojm::-webkit-scrollbar {width:0.5rem;}.panel-body.svelte-168eojm::-webkit-scrollbar-thumb {border-radius:999px;background:color-mix(in oklab, var(--color-base-content) 20%, transparent);}\n\n    /* One skill per card, mirroring the course cards in "My Learning". */.skill-row.svelte-168eojm {background:color-mix(in oklab, var(--color-base-200) 50%, transparent);border:1px solid color-mix(in oklab, var(--color-base-content) 8%, transparent);border-radius:1rem;padding:0.9rem 1.1rem;}.skill-head.svelte-168eojm {display:flex;align-items:center;justify-content:space-between;gap:0.75rem;margin-bottom:0.6rem;}.skill-name.svelte-168eojm {font-size:1.05rem;font-weight:700;color:var(--color-base-content);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}.skill-level.svelte-168eojm {flex:0 0 auto;font-size:0.75rem;font-weight:700;letter-spacing:0.03em;padding:0.15rem 0.6rem;border-radius:999px;color:var(--color-primary-content);background:var(--color-primary);box-shadow:0 0 12px color-mix(in oklab, var(--color-primary) 40%, transparent);}.skill-bar.svelte-168eojm {display:grid;grid-template-columns:1fr 3rem;align-items:center;gap:0.75rem;}.skill-percent.svelte-168eojm {font-weight:700;text-align:right;color:var(--color-base-content);}.empty.svelte-168eojm {color:color-mix(in oklab, var(--color-base-content) 60%, transparent);padding:1.5rem 0;}'
};
function SkillMatrixPanel($$anchor, $$props) {
  push($$props, true);
  append_styles($$anchor, $$css8);
  let skills = prop($$props, "skills", 7);
  const isEmpty = user_derived(() => skills().length === 0);
  var $$exports = {
    get skills() {
      return skills();
    },
    set skills($$value) {
      skills($$value);
      flushSync();
    }
  };
  var section = root_23();
  var div = sibling(child(section), 2);
  var node = child(div);
  {
    var consequent = ($$anchor2) => {
      var p = root8();
      append($$anchor2, p);
    };
    var alternate = ($$anchor2) => {
      var fragment = comment();
      var node_1 = first_child(fragment);
      each(node_1, 17, skills, (skill) => skill.id, ($$anchor3, skill) => {
        var div_1 = root_16();
        var div_2 = child(div_1);
        var span = child(div_2);
        var text2 = child(span, true);
        reset(span);
        var span_1 = sibling(span, 2);
        var text_1 = child(span_1);
        reset(span_1);
        reset(div_2);
        var div_3 = sibling(div_2, 2);
        var node_2 = child(div_3);
        {
          let $0 = user_derived(() => `${get2(skill).name} progress`);
          ProgressBar(node_2, {
            get value() {
              return get2(skill).progress;
            },
            get label() {
              return get2($0);
            }
          });
        }
        var span_2 = sibling(node_2, 2);
        var text_2 = child(span_2);
        reset(span_2);
        reset(div_3);
        reset(div_1);
        template_effect(
          ($0) => {
            set_text(text2, get2(skill).name);
            set_text(text_1, `Lv ${get2(skill).level ?? ""}`);
            set_text(text_2, `${$0 ?? ""}%`);
          },
          [() => Math.round(get2(skill).progress)]
        );
        append($$anchor3, div_1);
      });
      append($$anchor2, fragment);
    };
    if_block(node, ($$render) => {
      if (get2(isEmpty)) $$render(consequent);
      else $$render(alternate, -1);
    });
  }
  reset(div);
  reset(section);
  append($$anchor, section);
  return pop($$exports);
}
create_custom_element(SkillMatrixPanel, { skills: {} }, [], [], { mode: "open" });

// src/components/pages/DashboardPage.svelte
var root9 = from_html(`<div class="status svelte-wafcro" role="status" aria-live="polite"><span class="loading loading-spinner loading-lg"></span> <p>Loading your dashboard\u2026</p></div>`);
var root_17 = from_html(`<div class="status svelte-wafcro" role="alert"><p class="error svelte-wafcro"> </p> <button type="button" class="btn btn-primary btn-sm">Retry</button></div>`);
var root_24 = from_html(`<div class="grid svelte-wafcro"><div class="grid-main svelte-wafcro"><!></div> <div class="grid-side svelte-wafcro"><!> <!></div></div>`);
var root_33 = from_html(`<div class="dashboard svelte-wafcro"><header class="top svelte-wafcro"><h1 class="title svelte-wafcro"> </h1></header> <!></div>`);
var $$css9 = {
  hash: "svelte-wafcro",
  code: "\r\n    /* Fill ~90% of the viewport with little margin around the edges. */.dashboard.svelte-wafcro {flex:1;min-height:0;overflow-y:auto;display:flex;flex-direction:column;gap:1.25rem;width:90%;max-width:110rem;margin:0 auto;padding:1.25rem 0 0.5rem;}.top.svelte-wafcro {flex:0 0 auto;text-align:center;}.title.svelte-wafcro {font-size:clamp(1.6rem, 3.5vw, 2.6rem);font-weight:800;letter-spacing:0.04em;color:var(--color-base-content);text-shadow:0 0 24px color-mix(in oklab, var(--color-primary) 45%, transparent);}\r\n\r\n    /* Stretch so both columns share the available height. */.grid.svelte-wafcro {flex:1;min-height:0;display:grid;grid-template-columns:2fr 1fr;gap:1.25rem;align-items:stretch;}.grid-main.svelte-wafcro {display:flex;min-height:0;}.grid-side.svelte-wafcro {display:flex;flex-direction:column;gap:1.25rem;min-height:0;}.status.svelte-wafcro {display:flex;flex-direction:column;align-items:center;gap:1rem;padding:4rem 0;color:color-mix(in oklab, var(--color-base-content) 70%, transparent);}.error.svelte-wafcro {color:var(--color-error);font-weight:600;text-align:center;}\r\n\r\n    @media (max-width: 60rem) {.grid.svelte-wafcro {grid-template-columns:1fr;}\r\n    }"
};
function DashboardPage($$anchor, $$props) {
  push($$props, true);
  append_styles($$anchor, $$css9);
  let state3 = state(proxy({
    isLoading: true,
    errorMessage: "",
    user: null,
    stats: null,
    skills: [],
    courses: []
  }));
  onMount(() => {
    const unsubscribe = dashboardStore.subscribe((value) => {
      set(state3, value, true);
    });
    dashboardStore.refresh();
    return unsubscribe;
  });
  const handle = user_derived(() => get2(state3).user?.username ? `@${get2(state3).user.username}` : "@user");
  var div = root_33();
  var header = child(div);
  var h1 = child(header);
  var text2 = child(h1);
  reset(h1);
  reset(header);
  var node = sibling(header, 2);
  {
    var consequent = ($$anchor2) => {
      var div_1 = root9();
      append($$anchor2, div_1);
    };
    var consequent_1 = ($$anchor2) => {
      var div_2 = root_17();
      var p = child(div_2);
      var text_1 = child(p, true);
      reset(p);
      var button = sibling(p, 2);
      reset(div_2);
      template_effect(() => set_text(text_1, get2(state3).errorMessage));
      delegated("click", button, () => dashboardStore.refresh());
      append($$anchor2, div_2);
    };
    var alternate = ($$anchor2) => {
      var div_3 = root_24();
      var div_4 = child(div_3);
      var node_1 = child(div_4);
      MyLearningPanel(node_1, {
        get courses() {
          return get2(state3).courses;
        },
        get skills() {
          return get2(state3).skills;
        },
        onCourseOpen: (course) => push2(`/chat/${course.id}`)
      });
      reset(div_4);
      var div_5 = sibling(div_4, 2);
      var node_2 = child(div_5);
      StatsPanel(node_2, {
        get user() {
          return get2(state3).user;
        },
        get stats() {
          return get2(state3).stats;
        },
        onProfile: () => push2("/profile")
      });
      var node_3 = sibling(node_2, 2);
      SkillMatrixPanel(node_3, {
        get skills() {
          return get2(state3).skills;
        }
      });
      reset(div_5);
      reset(div_3);
      append($$anchor2, div_3);
    };
    if_block(node, ($$render) => {
      if (get2(state3).isLoading) $$render(consequent);
      else if (get2(state3).errorMessage) $$render(consequent_1, 1);
      else $$render(alternate, -1);
    });
  }
  reset(div);
  template_effect(() => set_text(text2, `${get2(handle) ?? ""} Dashboard`));
  append($$anchor, div);
  pop();
}
delegate(["click"]);
create_custom_element(DashboardPage, {}, [], [], { mode: "open" });

// src/api/profile.ts
async function saveProfile(username, fields, picture) {
  const path = `/api/auth/users/${encodeURIComponent(username)}/`;
  if (picture) {
    const form = new FormData();
    form.set("first_name", fields.firstName);
    form.set("last_name", fields.lastName);
    form.set("description", fields.description);
    form.set("picture", picture);
    await apiSend("PATCH", path, form, { formData: true });
    return;
  }
  await apiSend("PATCH", path, {
    first_name: fields.firstName,
    last_name: fields.lastName,
    description: fields.description
  });
}
async function fetchEmailAddresses() {
  const response = await apiGet("/auth-api/browser/v1/account/email");
  return response.data ?? [];
}
async function requestEmailChange(email) {
  await apiSend("POST", "/auth-api/browser/v1/account/email", { email });
}

// src/components/pages/ProfileEditPage.svelte
var root10 = from_html(`<div class="status svelte-1u1012d" role="status" aria-live="polite"><span class="loading loading-spinner loading-lg"></span> <p>Loading your profile\u2026</p></div>`);
var root_18 = from_html(`<div class="status svelte-1u1012d" role="alert"><p class="error svelte-1u1012d"> </p></div>`);
var root_25 = from_html(`<img alt="" class="svelte-1u1012d"/>`);
var root_34 = from_html(`<span class="badge badge-sm badge-primary">primary</span>`);
var root_43 = from_html(`<li class="svelte-1u1012d"> <span> </span> <!></li>`);
var root_52 = from_html(`<ul class="email-list svelte-1u1012d"></ul>`);
var root_62 = from_html(`<p class="error svelte-1u1012d" role="alert"> </p>`);
var root_7 = from_html(`<p class="success svelte-1u1012d" role="status"> </p>`);
var root_8 = from_html(`<span class="loading loading-spinner loading-sm"></span>`);
var root_9 = from_html(`<form class="card form svelte-1u1012d"><div class="avatar-row svelte-1u1012d"><span class="avatar-mark svelte-1u1012d" aria-hidden="true"><!></span> <div class="avatar-actions svelte-1u1012d"><label class="field-label svelte-1u1012d" for="picture">Profile picture</label> <input id="picture" class="file-input file-input-bordered file-input-sm" type="file" accept="image/*"/></div></div> <label class="field svelte-1u1012d"><span class="field-label svelte-1u1012d">Username</span> <input class="input input-bordered" type="text" readonly=""/> <span class="hint svelte-1u1012d">Username cannot be changed.</span></label> <div class="two-col svelte-1u1012d"><label class="field svelte-1u1012d"><span class="field-label svelte-1u1012d">First name</span> <input class="input input-bordered" type="text" autocomplete="given-name"/></label> <label class="field svelte-1u1012d"><span class="field-label svelte-1u1012d">Last name</span> <input class="input input-bordered" type="text" autocomplete="family-name"/></label></div> <label class="field svelte-1u1012d"><span class="field-label svelte-1u1012d">Description</span> <textarea class="textarea textarea-bordered" rows="4"></textarea></label> <label class="field svelte-1u1012d"><span class="field-label svelte-1u1012d">E-mail</span> <input class="input input-bordered" type="email" autocomplete="email"/> <span class="hint svelte-1u1012d">Changing your e-mail sends a verification link; it activates after you confirm.</span></label> <!> <!> <!> <div class="actions svelte-1u1012d"><button type="submit" class="btn btn-primary"><!> Save changes</button></div></form>`);
var root_10 = from_html(`<div class="profile svelte-1u1012d"><header class="head svelte-1u1012d"><h1 class="title svelte-1u1012d">Edit Profile</h1> <button type="button" class="btn btn-ghost btn-sm">\u2190 Back to Dashboard</button></header> <!></div>`);
var $$css10 = {
  hash: "svelte-1u1012d",
  code: ".profile.svelte-1u1012d {flex:1;min-height:0;overflow-y:auto;max-width:42rem;width:100%;margin:0 auto;padding:2rem 1.5rem 1rem;display:flex;flex-direction:column;gap:1.5rem;}.head.svelte-1u1012d {display:flex;align-items:center;justify-content:space-between;gap:1rem;}.title.svelte-1u1012d {font-size:1.6rem;font-weight:800;color:var(--color-base-content);}.form.svelte-1u1012d {background:var(--color-base-100);border-radius:1rem;padding:1.5rem;display:flex;flex-direction:column;gap:1.1rem;box-shadow:0 0 24px color-mix(in oklab, var(--color-primary) 10%, transparent);}.avatar-row.svelte-1u1012d {display:flex;align-items:center;gap:1rem;}.avatar-mark.svelte-1u1012d {width:4rem;height:4rem;flex:0 0 auto;border-radius:999px;overflow:hidden;background:color-mix(in oklab, var(--color-base-content) 18%, transparent);box-shadow:0 0 16px color-mix(in oklab, var(--color-primary) 30%, transparent);}.avatar-mark.svelte-1u1012d img:where(.svelte-1u1012d) {width:100%;height:100%;object-fit:cover;}.avatar-actions.svelte-1u1012d {display:flex;flex-direction:column;gap:0.35rem;}.field.svelte-1u1012d {display:flex;flex-direction:column;gap:0.35rem;}.field-label.svelte-1u1012d {font-size:0.85rem;font-weight:600;color:color-mix(in oklab, var(--color-base-content) 80%, transparent);}.two-col.svelte-1u1012d {display:grid;grid-template-columns:1fr 1fr;gap:1rem;}.hint.svelte-1u1012d {font-size:0.75rem;color:color-mix(in oklab, var(--color-base-content) 60%, transparent);}.email-list.svelte-1u1012d {list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:0.35rem;font-size:0.85rem;color:var(--color-base-content);}.email-list.svelte-1u1012d li:where(.svelte-1u1012d) {display:flex;align-items:center;gap:0.5rem;}.error.svelte-1u1012d {color:var(--color-error);font-weight:600;}.success.svelte-1u1012d {color:var(--color-success);font-weight:600;}.status.svelte-1u1012d {display:flex;flex-direction:column;align-items:center;gap:1rem;padding:4rem 0;color:color-mix(in oklab, var(--color-base-content) 70%, transparent);}.actions.svelte-1u1012d {display:flex;justify-content:flex-end;}\r\n\r\n    @media (max-width: 40rem) {.two-col.svelte-1u1012d {grid-template-columns:1fr;}\r\n    }"
};
function ProfileEditPage($$anchor, $$props) {
  push($$props, true);
  append_styles($$anchor, $$css10);
  let isLoading = state(true);
  let isSaving = state(false);
  let errorMessage = state("");
  let successMessage = state("");
  let username = state("");
  let firstName = state("");
  let lastName = state("");
  let description = state("");
  let email = state("");
  let originalEmail = state("");
  let currentPictureUrl = state(null);
  let previewUrl = state(null);
  let pictureFile = state(null);
  let emails = state(proxy([]));
  const previewSrc = user_derived(() => get2(previewUrl) ?? get2(currentPictureUrl));
  async function load() {
    const user = await fetchCurrentUser();
    if (!user || !user.is_authenticated) {
      throw new Error("You are not signed in. Please log in to edit your profile.");
    }
    set(username, user.username, true);
    set(firstName, user.first_name ?? "", true);
    set(lastName, user.last_name ?? "", true);
    set(description, user.description ?? "", true);
    set(email, user.email ?? "", true);
    set(originalEmail, user.email ?? "", true);
    set(currentPictureUrl, user.picture ?? null, true);
    set(emails, await fetchEmailAddresses().catch(() => []), true);
  }
  onMount(() => {
    load().catch((error) => {
      set(errorMessage, error instanceof Error ? error.message : String(error), true);
    }).finally(() => {
      set(isLoading, false);
    });
  });
  onDestroy(() => {
    if (get2(previewUrl)) {
      URL.revokeObjectURL(get2(previewUrl));
    }
  });
  function onPickFile(event2) {
    const input = event2.currentTarget;
    const file = input.files?.[0] ?? null;
    if (get2(previewUrl)) {
      URL.revokeObjectURL(get2(previewUrl));
    }
    set(pictureFile, file, true);
    set(previewUrl, file ? URL.createObjectURL(file) : null, true);
  }
  async function save2() {
    if (!get2(username) || get2(isSaving)) {
      return;
    }
    set(isSaving, true);
    set(errorMessage, "");
    set(successMessage, "");
    try {
      await saveProfile(
        get2(username),
        {
          firstName: get2(firstName),
          lastName: get2(lastName),
          description: get2(description)
        },
        get2(pictureFile)
      );
      let message = "Profile saved.";
      if (get2(email) && get2(email) !== get2(originalEmail)) {
        await requestEmailChange(get2(email));
        message += " A verification link was sent to the new e-mail address.";
      }
      if (get2(previewUrl)) {
        URL.revokeObjectURL(get2(previewUrl));
      }
      set(pictureFile, null);
      set(previewUrl, null);
      await dashboardStore.refresh();
      await load();
      set(successMessage, message, true);
    } catch (error) {
      set(errorMessage, error instanceof Error ? error.message : String(error), true);
    } finally {
      set(isSaving, false);
    }
  }
  var div = root_10();
  var header = child(div);
  var button = sibling(child(header), 2);
  reset(header);
  var node = sibling(header, 2);
  {
    var consequent = ($$anchor2) => {
      var div_1 = root10();
      append($$anchor2, div_1);
    };
    var consequent_1 = ($$anchor2) => {
      var div_2 = root_18();
      var p = child(div_2);
      var text2 = child(p, true);
      reset(p);
      reset(div_2);
      template_effect(() => set_text(text2, get2(errorMessage)));
      append($$anchor2, div_2);
    };
    var alternate = ($$anchor2) => {
      var form = root_9();
      var div_3 = child(form);
      var span = child(div_3);
      var node_1 = child(span);
      {
        var consequent_2 = ($$anchor3) => {
          var img = root_25();
          template_effect(() => set_attribute2(img, "src", get2(previewSrc)));
          append($$anchor3, img);
        };
        if_block(node_1, ($$render) => {
          if (get2(previewSrc)) $$render(consequent_2);
        });
      }
      reset(span);
      var div_4 = sibling(span, 2);
      var input_1 = sibling(child(div_4), 2);
      reset(div_4);
      reset(div_3);
      var label = sibling(div_3, 2);
      var input_2 = sibling(child(label), 2);
      remove_input_defaults(input_2);
      next(2);
      reset(label);
      var div_5 = sibling(label, 2);
      var label_1 = child(div_5);
      var input_3 = sibling(child(label_1), 2);
      remove_input_defaults(input_3);
      reset(label_1);
      var label_2 = sibling(label_1, 2);
      var input_4 = sibling(child(label_2), 2);
      remove_input_defaults(input_4);
      reset(label_2);
      reset(div_5);
      var label_3 = sibling(div_5, 2);
      var textarea = sibling(child(label_3), 2);
      remove_textarea_child(textarea);
      reset(label_3);
      var label_4 = sibling(label_3, 2);
      var input_5 = sibling(child(label_4), 2);
      remove_input_defaults(input_5);
      next(2);
      reset(label_4);
      var node_2 = sibling(label_4, 2);
      {
        var consequent_4 = ($$anchor3) => {
          var ul = root_52();
          each(ul, 21, () => get2(emails), (entry) => entry.email, ($$anchor4, entry) => {
            var li = root_43();
            var text_1 = child(li);
            var span_1 = sibling(text_1);
            var text_2 = child(span_1, true);
            reset(span_1);
            var node_3 = sibling(span_1, 2);
            {
              var consequent_3 = ($$anchor5) => {
                var span_2 = root_34();
                append($$anchor5, span_2);
              };
              if_block(node_3, ($$render) => {
                if (get2(entry).primary) $$render(consequent_3);
              });
            }
            reset(li);
            template_effect(() => {
              set_text(text_1, `${get2(entry).email ?? ""} `);
              set_class(span_1, 1, `badge badge-sm ${get2(entry).verified ? "badge-success" : "badge-warning"}`);
              set_text(text_2, get2(entry).verified ? "verified" : "unverified");
            });
            append($$anchor4, li);
          });
          reset(ul);
          append($$anchor3, ul);
        };
        if_block(node_2, ($$render) => {
          if (get2(emails).length > 0) $$render(consequent_4);
        });
      }
      var node_4 = sibling(node_2, 2);
      {
        var consequent_5 = ($$anchor3) => {
          var p_1 = root_62();
          var text_3 = child(p_1, true);
          reset(p_1);
          template_effect(() => set_text(text_3, get2(errorMessage)));
          append($$anchor3, p_1);
        };
        if_block(node_4, ($$render) => {
          if (get2(errorMessage)) $$render(consequent_5);
        });
      }
      var node_5 = sibling(node_4, 2);
      {
        var consequent_6 = ($$anchor3) => {
          var p_2 = root_7();
          var text_4 = child(p_2, true);
          reset(p_2);
          template_effect(() => set_text(text_4, get2(successMessage)));
          append($$anchor3, p_2);
        };
        if_block(node_5, ($$render) => {
          if (get2(successMessage)) $$render(consequent_6);
        });
      }
      var div_6 = sibling(node_5, 2);
      var button_1 = child(div_6);
      var node_6 = child(button_1);
      {
        var consequent_7 = ($$anchor3) => {
          var span_3 = root_8();
          append($$anchor3, span_3);
        };
        if_block(node_6, ($$render) => {
          if (get2(isSaving)) $$render(consequent_7);
        });
      }
      next();
      reset(button_1);
      reset(div_6);
      reset(form);
      template_effect(() => {
        set_value(input_2, get2(username));
        button_1.disabled = get2(isSaving);
      });
      event("submit", form, (event2) => {
        event2.preventDefault();
        save2();
      });
      delegated("change", input_1, onPickFile);
      bind_value(input_3, () => get2(firstName), ($$value) => set(firstName, $$value));
      bind_value(input_4, () => get2(lastName), ($$value) => set(lastName, $$value));
      bind_value(textarea, () => get2(description), ($$value) => set(description, $$value));
      bind_value(input_5, () => get2(email), ($$value) => set(email, $$value));
      append($$anchor2, form);
    };
    if_block(node, ($$render) => {
      if (get2(isLoading)) $$render(consequent);
      else if (get2(errorMessage) && !get2(username)) $$render(consequent_1, 1);
      else $$render(alternate, -1);
    });
  }
  reset(div);
  delegated("click", button, () => push2("/"));
  append($$anchor, div);
  pop();
}
delegate(["click", "change"]);
create_custom_element(ProfileEditPage, {}, [], [], { mode: "open" });

// src/components/pages/CourseChatPage.svelte
var root11 = from_html(`<span class="soon svelte-nqv0rv">soon</span>`);
var root_19 = from_html(`<button type="button" class="nav-item svelte-nqv0rv"><span class="nav-icon svelte-nqv0rv" aria-hidden="true"> </span> <span class="nav-label svelte-nqv0rv"> </span> <!></button>`);
var root_26 = from_html(`<img class="avatar svelte-nqv0rv" src="logo.png" alt="ElisaAI assistant"/>`);
var root_35 = from_html(`<div><!> <div> </div></div>`);
var root_44 = from_html(`<div class="error-overlay svelte-nqv0rv" role="alert"><div class="error-card svelte-nqv0rv"><span class="error-icon svelte-nqv0rv" aria-hidden="true">\u{1F50C}</span> <h2 class="error-title svelte-nqv0rv">Assistant unavailable</h2> <p class="error-text svelte-nqv0rv"> </p> <button type="button" class="btn btn-primary">Retry</button></div></div>`);
var root_53 = from_html(`<div class="chat-screen svelte-nqv0rv"><aside class="sidebar svelte-nqv0rv"><button type="button" class="back svelte-nqv0rv">\u2190 Dashboard</button> <button type="button" class="content-cta svelte-nqv0rv"><span aria-hidden="true">\u{1F4D6}</span> <span>Content</span></button> <nav class="nav svelte-nqv0rv" aria-label="Sections"></nav></aside> <main class="conversation svelte-nqv0rv"><div class="messages svelte-nqv0rv"><div class="message svelte-nqv0rv"><img class="avatar svelte-nqv0rv" src="logo.png" alt="ElisaAI assistant"/> <div class="bubble svelte-nqv0rv">System online. I am <strong>ElisaAI</strong>. Ready to help you with <strong> </strong> \u2014 what topic shall we analyse today?</div></div> <!></div> <div class="composer svelte-nqv0rv"><span><span class="status-dot svelte-nqv0rv" aria-hidden="true"></span> </span> <form class="composer-row svelte-nqv0rv"><button type="button" class="composer-add svelte-nqv0rv" aria-label="Add attachment" disabled="">+</button> <input class="composer-input svelte-nqv0rv" type="text"/> <button type="submit" class="composer-send svelte-nqv0rv" aria-label="Send message">\u2192</button></form> <p class="disclaimer svelte-nqv0rv">ElisaAI 2026 // ElisaAI may generate misinformation. Please verify all information.</p></div> <!></main></div>`);
var $$css11 = {
  hash: "svelte-nqv0rv",
  code: ".chat-screen.svelte-nqv0rv {flex:1;min-height:0;overflow:hidden;display:grid;grid-template-columns:16rem 1fr;grid-template-rows:minmax(0, 1fr);width:100%;}\r\n\r\n    /* Sidebar stays put; only the conversation scrolls. */.sidebar.svelte-nqv0rv {min-height:0;overflow:hidden;display:flex;flex-direction:column;gap:1.5rem;padding:1.5rem 1rem;border-right:1px solid color-mix(in oklab, var(--color-base-content) 10%, transparent);background:color-mix(in oklab, var(--color-base-100) 60%, transparent);}.back.svelte-nqv0rv {align-self:flex-start;background:none;border:none;cursor:pointer;font-weight:600;color:var(--color-primary);}.back.svelte-nqv0rv:focus-visible {outline:2px solid var(--color-primary);outline-offset:2px;}.content-cta.svelte-nqv0rv {display:flex;align-items:center;justify-content:center;gap:0.5rem;padding:0.85rem 1rem;border-radius:0.85rem;border:1px solid color-mix(in oklab, var(--color-primary) 55%, transparent);font-size:1.05rem;font-weight:700;cursor:pointer;color:var(--color-primary-content);background:var(--color-primary);box-shadow:0 0 18px color-mix(in oklab, var(--color-primary) 45%, transparent);transition:transform 0.12s ease;}.content-cta.svelte-nqv0rv:hover {transform:translateY(-2px);}.content-cta.svelte-nqv0rv:focus-visible {outline:2px solid var(--color-base-content);outline-offset:2px;}.nav.svelte-nqv0rv {display:flex;flex-direction:column;gap:0.35rem;}.nav-item.svelte-nqv0rv {display:flex;align-items:center;gap:0.75rem;padding:0.65rem 0.75rem;border-radius:0.75rem;background:transparent;border:none;color:var(--color-base-content);cursor:pointer;}.nav-item.svelte-nqv0rv:hover:not(:disabled) {background:color-mix(in oklab, var(--color-primary) 14%, transparent);}.nav-item.svelte-nqv0rv:focus-visible {outline:2px solid var(--color-primary);outline-offset:2px;}.nav-item.svelte-nqv0rv:disabled {cursor:not-allowed;opacity:0.6;}.nav-icon.svelte-nqv0rv {font-size:1.1rem;}.nav-label.svelte-nqv0rv {flex:1 1 auto;text-align:left;font-weight:600;}.soon.svelte-nqv0rv {font-size:0.65rem;text-transform:uppercase;letter-spacing:0.06em;color:color-mix(in oklab, var(--color-base-content) 50%, transparent);}.conversation.svelte-nqv0rv {position:relative;display:flex;flex-direction:column;min-height:0;background:var(--color-base-200);}.messages.svelte-nqv0rv {flex:1;min-height:0;overflow-y:auto;display:flex;flex-direction:column;gap:1.25rem;padding:2rem clamp(1rem, 6vw, 6rem);}.message.svelte-nqv0rv {display:flex;align-items:flex-start;gap:0.85rem;max-width:56rem;}.message.user.svelte-nqv0rv {margin-left:auto;justify-content:flex-end;}.avatar.svelte-nqv0rv {width:2.75rem;height:2.75rem;flex:0 0 auto;border-radius:999px;object-fit:cover;}.bubble.svelte-nqv0rv {padding:1rem 1.25rem;border-radius:1rem;border-top-left-radius:0.25rem;line-height:1.55;color:var(--color-base-content);background:color-mix(in oklab, var(--color-base-100) 85%, transparent);border:1px solid color-mix(in oklab, var(--color-primary) 30%, transparent);box-shadow:0 0 18px color-mix(in oklab, var(--color-primary) 12%, transparent);white-space:pre-wrap;}.bubble.user.svelte-nqv0rv {color:var(--color-primary-content);background:var(--color-primary);border-color:transparent;border-top-left-radius:1rem;border-bottom-right-radius:0.25rem;}.composer.svelte-nqv0rv {flex:0 0 auto;display:flex;flex-direction:column;gap:0.5rem;padding:1rem clamp(1rem, 6vw, 6rem) 1.25rem;}.status.svelte-nqv0rv {align-self:center;display:inline-flex;align-items:center;gap:0.4rem;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.06em;color:color-mix(in oklab, var(--color-base-content) 60%, transparent);}.status-dot.svelte-nqv0rv {width:0.5rem;height:0.5rem;border-radius:999px;background:color-mix(in oklab, var(--color-base-content) 40%, transparent);}.status.online.svelte-nqv0rv {color:var(--color-success);}\r\n\r\n    /* Centered overlay shown when the assistant connection gives up. */.error-overlay.svelte-nqv0rv {position:absolute;inset:0;z-index:5;display:grid;place-items:center;padding:1.5rem;background:color-mix(in oklab, var(--color-base-300) 55%, transparent);backdrop-filter:blur(4px);}.error-card.svelte-nqv0rv {display:flex;flex-direction:column;align-items:center;gap:0.85rem;max-width:26rem;width:100%;text-align:center;padding:2rem;border-radius:1.25rem;background:var(--color-base-100);border:1px solid color-mix(in oklab, var(--color-warning) 35%, transparent);box-shadow:0 0 40px color-mix(in oklab, var(--color-warning) 18%, transparent);}.error-icon.svelte-nqv0rv {font-size:2.5rem;line-height:1;}.error-title.svelte-nqv0rv {font-size:1.3rem;font-weight:700;color:var(--color-base-content);}.error-text.svelte-nqv0rv {line-height:1.5;color:color-mix(in oklab, var(--color-base-content) 75%, transparent);}.status.online.svelte-nqv0rv .status-dot:where(.svelte-nqv0rv) {background:var(--color-success);box-shadow:0 0 10px color-mix(in oklab, var(--color-success) 70%, transparent);}.composer-row.svelte-nqv0rv {display:flex;align-items:center;gap:0.75rem;padding:0.5rem 0.75rem;border-radius:999px;background:color-mix(in oklab, var(--color-base-100) 80%, transparent);border:1px solid color-mix(in oklab, var(--color-primary) 35%, transparent);box-shadow:0 0 18px color-mix(in oklab, var(--color-primary) 12%, transparent);}.composer-add.svelte-nqv0rv,\r\n    .composer-send.svelte-nqv0rv {display:grid;place-items:center;width:2.25rem;height:2.25rem;flex:0 0 auto;border-radius:999px;border:none;font-size:1.2rem;cursor:pointer;color:var(--color-primary-content);background:color-mix(in oklab, var(--color-primary) 70%, transparent);}.composer-add.svelte-nqv0rv:disabled,\r\n    .composer-send.svelte-nqv0rv:disabled {cursor:not-allowed;opacity:0.6;}.composer-input.svelte-nqv0rv {flex:1 1 auto;background:transparent;border:none;color:var(--color-base-content);font-size:1rem;padding:0.5rem 0.25rem;}.composer-input.svelte-nqv0rv:focus {outline:none;}.disclaimer.svelte-nqv0rv {text-align:center;font-size:0.7rem;letter-spacing:0.04em;color:color-mix(in oklab, var(--color-base-content) 55%, transparent);}\r\n\r\n    @media (max-width: 48rem) {.chat-screen.svelte-nqv0rv {grid-template-columns:1fr;}.sidebar.svelte-nqv0rv {display:none;}\r\n    }"
};
function CourseChatPage($$anchor, $$props) {
  push($$props, true);
  append_styles($$anchor, $$css11);
  let params = prop($$props, "params", 7);
  let state3 = state(proxy({
    isLoading: true,
    errorMessage: "",
    user: null,
    stats: null,
    skills: [],
    courses: []
  }));
  let chat;
  let chatState = state(proxy({ connection: "disconnected", errorMessage: "", messages: [] }));
  let draft = state("");
  onMount(() => {
    const unsubscribeDashboard = dashboardStore.subscribe((value) => {
      set(state3, value, true);
    });
    if (get2(state3).courses.length === 0) {
      dashboardStore.refresh();
    }
    chat = createAiChatStore(params()?.id);
    const unsubscribeChat = chat.subscribe((value) => {
      set(chatState, value, true);
    });
    void chat.connect();
    return () => {
      unsubscribeDashboard();
      unsubscribeChat();
      void chat?.disconnect();
    };
  });
  const courseName2 = user_derived(() => get2(state3).courses.find((course) => course.id === params()?.id)?.name ?? "this course");
  const navItems = user_derived(() => [
    { icon: "\u{1F3AE}", label: "Games" },
    {
      icon: "\u{1F9E0}",
      label: "Quizzes",
      to: `/quiz/${params()?.id ?? ""}`
    },
    { icon: "\u{1F393}", label: "Exams" },
    { icon: "\u{1F4AC}", label: "Chats" }
  ]);
  const connected = user_derived(() => get2(chatState).connection === "connected");
  const statusLabel = user_derived(() => get2(chatState).connection === "connected" ? "Online" : get2(chatState).connection === "connecting" ? "Connecting\u2026" : get2(chatState).connection === "wait_before_retry" ? "Reconnecting\u2026" : "Offline");
  async function send() {
    const text2 = get2(draft).trim();
    if (!text2 || !get2(connected)) {
      return;
    }
    set(draft, "");
    await chat?.sendChatInput("markdown", text2);
  }
  var $$exports = {
    get params() {
      return params();
    },
    set params($$value) {
      params($$value);
      flushSync();
    }
  };
  var div = root_53();
  var aside = child(div);
  var button = child(aside);
  var button_1 = sibling(button, 2);
  var nav = sibling(button_1, 2);
  each(nav, 21, () => get2(navItems), (item) => item.label, ($$anchor2, item) => {
    var button_2 = root_19();
    var span = child(button_2);
    var text_1 = child(span, true);
    reset(span);
    var span_1 = sibling(span, 2);
    var text_2 = child(span_1, true);
    reset(span_1);
    var node = sibling(span_1, 2);
    {
      var consequent = ($$anchor3) => {
        var span_2 = root11();
        append($$anchor3, span_2);
      };
      if_block(node, ($$render) => {
        if (!get2(item).to) $$render(consequent);
      });
    }
    reset(button_2);
    template_effect(() => {
      button_2.disabled = !get2(item).to;
      set_text(text_1, get2(item).icon);
      set_text(text_2, get2(item).label);
    });
    delegated("click", button_2, () => get2(item).to && push2(get2(item).to));
    append($$anchor2, button_2);
  });
  reset(nav);
  reset(aside);
  var main = sibling(aside, 2);
  var div_1 = child(main);
  var div_2 = child(div_1);
  var div_3 = sibling(child(div_2), 2);
  var strong = sibling(child(div_3), 3);
  var text_3 = child(strong, true);
  reset(strong);
  next();
  reset(div_3);
  reset(div_2);
  var node_1 = sibling(div_2, 2);
  each(node_1, 17, () => get2(chatState).messages, (message) => message.id, ($$anchor2, message) => {
    var div_4 = root_35();
    let classes;
    var node_2 = child(div_4);
    {
      var consequent_1 = ($$anchor3) => {
        var img = root_26();
        append($$anchor3, img);
      };
      if_block(node_2, ($$render) => {
        if (get2(message).sender === "assistant") $$render(consequent_1);
      });
    }
    var div_5 = sibling(node_2, 2);
    let classes_1;
    var text_4 = child(div_5, true);
    reset(div_5);
    reset(div_4);
    template_effect(() => {
      classes = set_class(div_4, 1, "message svelte-nqv0rv", null, classes, { user: get2(message).sender === "user" });
      classes_1 = set_class(div_5, 1, "bubble svelte-nqv0rv", null, classes_1, { user: get2(message).sender === "user" });
      set_text(text_4, get2(message).content);
    });
    append($$anchor2, div_4);
  });
  reset(div_1);
  var div_6 = sibling(div_1, 2);
  var span_3 = child(div_6);
  let classes_2;
  var text_5 = sibling(child(span_3));
  reset(span_3);
  var form = sibling(span_3, 2);
  var input = sibling(child(form), 2);
  remove_input_defaults(input);
  var button_3 = sibling(input, 2);
  reset(form);
  next(2);
  reset(div_6);
  var node_3 = sibling(div_6, 2);
  {
    var consequent_2 = ($$anchor2) => {
      var div_7 = root_44();
      var div_8 = child(div_7);
      var p = sibling(child(div_8), 4);
      var text_6 = child(p, true);
      reset(p);
      var button_4 = sibling(p, 2);
      reset(div_8);
      reset(div_7);
      template_effect(() => set_text(text_6, get2(chatState).errorMessage));
      delegated("click", button_4, () => chat?.retry());
      append($$anchor2, div_7);
    };
    if_block(node_3, ($$render) => {
      if (get2(chatState).errorMessage) $$render(consequent_2);
    });
  }
  reset(main);
  reset(div);
  template_effect(
    ($0) => {
      set_text(text_3, get2(courseName2));
      classes_2 = set_class(span_3, 1, "status svelte-nqv0rv", null, classes_2, { online: get2(connected) });
      set_text(text_5, ` ${get2(statusLabel) ?? ""}`);
      set_attribute2(input, "placeholder", get2(connected) ? "Message" : "Connecting\u2026");
      input.disabled = !get2(connected);
      button_3.disabled = $0;
    },
    [() => !get2(connected) || get2(draft).trim().length === 0]
  );
  delegated("click", button, () => push2("/"));
  delegated("click", button_1, () => push2(`/content/${params()?.id ?? ""}`));
  event("submit", form, (event2) => {
    event2.preventDefault();
    send();
  });
  bind_value(input, () => get2(draft), ($$value) => set(draft, $$value));
  append($$anchor, div);
  return pop($$exports);
}
delegate(["click"]);
create_custom_element(CourseChatPage, { params: {} }, [], [], { mode: "open" });

// src/components/pages/QuizPage.svelte
var root12 = from_html(`<div class="progress-track svelte-10mivl5" aria-hidden="true"><div class="progress-fill svelte-10mivl5"></div></div>`);
var root_110 = from_html(`<section class="stage result svelte-10mivl5"><h1 class="course svelte-10mivl5"> </h1> <div class="score-ring svelte-10mivl5"> </div> <p class="result-text svelte-10mivl5"> </p> <div class="result-actions svelte-10mivl5"><button type="button" class="btn btn-primary">Try again</button> <button type="button" class="btn btn-ghost">Back to Dashboard</button></div></section>`);
var root_27 = from_html(`<button type="button"><span class="letter svelte-10mivl5"> </span> <span class="text svelte-10mivl5"> </span></button>`);
var root_36 = from_html(`<section class="stage svelte-10mivl5"><h1 class="course svelte-10mivl5"> </h1> <span class="progress-pill svelte-10mivl5"> </span> <h2 class="prompt svelte-10mivl5"> </h2> <div class="answers svelte-10mivl5"></div></section>`);
var root_45 = from_html(`<div class="quiz svelte-10mivl5"><header class="quiz-top svelte-10mivl5"><button type="button" class="content-btn svelte-10mivl5">\u2190 Back</button> <!></header> <!></div>`);
var $$css12 = {
  hash: "svelte-10mivl5",
  code: '.quiz.svelte-10mivl5 {flex:1;min-height:0;display:flex;flex-direction:column;width:100%;background:radial-gradient(120% 70% at 50% 0%, color-mix(in oklab, var(--color-primary) 8%, transparent), transparent 55%),\r\n            var(--color-base-200);}.quiz-top.svelte-10mivl5 {flex:0 0 auto;display:flex;align-items:center;gap:1.5rem;padding:1.25rem 1.5rem;}.content-btn.svelte-10mivl5 {flex:0 0 auto;padding:0.5rem 1.25rem;border-radius:0.75rem;font-weight:600;color:color-mix(in oklab, var(--color-base-content) 80%, transparent);background:color-mix(in oklab, var(--color-base-100) 70%, transparent);border:1px solid color-mix(in oklab, var(--color-base-content) 14%, transparent);cursor:pointer;}.content-btn.svelte-10mivl5:hover {border-color:color-mix(in oklab, var(--color-primary) 45%, transparent);}.progress-track.svelte-10mivl5 {flex:1 1 auto;height:0.5rem;border-radius:999px;overflow:hidden;background:color-mix(in oklab, var(--color-base-content) 12%, transparent);}.progress-fill.svelte-10mivl5 {height:100%;border-radius:999px;background:linear-gradient(90deg, var(--color-primary), var(--color-success));transition:width 0.3s ease;}.stage.svelte-10mivl5 {flex:1;min-height:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1.25rem;width:90%;max-width:64rem;margin:0 auto;padding:1rem 0 2.5rem;}.course.svelte-10mivl5 {font-size:clamp(1.3rem, 2.4vw, 1.9rem);font-weight:700;text-align:center;color:var(--color-base-content);text-shadow:0 0 20px color-mix(in oklab, var(--color-primary) 40%, transparent);}.progress-pill.svelte-10mivl5 {padding:0.3rem 1rem;border-radius:999px;font-weight:700;color:var(--color-primary);background:color-mix(in oklab, var(--color-primary) 16%, transparent);border:1px solid color-mix(in oklab, var(--color-primary) 35%, transparent);}.prompt.svelte-10mivl5 {font-size:clamp(1.7rem, 3.6vw, 2.8rem);font-weight:800;text-align:center;color:var(--color-base-content);text-shadow:0 0 22px color-mix(in oklab, var(--color-primary) 35%, transparent);margin:0.5rem 0 1rem;}.answers.svelte-10mivl5 {width:100%;display:grid;grid-template-columns:1fr 1fr;gap:1.1rem;}\r\n\r\n    /* Answer colours map to DaisyUI semantic tokens (no hardcoded hex). */.answer.svelte-10mivl5 {display:flex;align-items:center;gap:1rem;padding:1.4rem 1.5rem;border-radius:1rem;border:none;font-family:ui-monospace, "SF Mono", Menlo, monospace;font-size:1.2rem;font-weight:700;cursor:pointer;transition:transform 0.12s ease, opacity 0.2s ease, box-shadow 0.2s ease;box-shadow:0 6px 18px color-mix(in oklab, var(--color-base-content) 14%, transparent);}.answer.svelte-10mivl5:hover:not(:disabled) {transform:translateY(-3px);}.answer.svelte-10mivl5:focus-visible {outline:3px solid var(--color-base-content);outline-offset:3px;}.letter.svelte-10mivl5 {display:grid;place-items:center;width:2.1rem;height:2.1rem;flex:0 0 auto;border-radius:0.6rem;font-family:inherit;background:color-mix(in oklab, currentColor 18%, transparent);}.text.svelte-10mivl5 {flex:1 1 auto;text-align:center;}.answer.c0.svelte-10mivl5 {background:var(--color-error);color:var(--color-error-content);}.answer.c1.svelte-10mivl5 {background:var(--color-info);color:var(--color-info-content);}.answer.c2.svelte-10mivl5 {background:var(--color-warning);color:var(--color-warning-content);}.answer.c3.svelte-10mivl5 {background:var(--color-success);color:var(--color-success-content);}.answer.dim.svelte-10mivl5 {opacity:0.35;}.answer.correct.svelte-10mivl5 {outline:4px solid var(--color-base-content);outline-offset:3px;transform:translateY(-3px);}.answer.wrong.svelte-10mivl5 {opacity:0.65;text-decoration:line-through;}.result.svelte-10mivl5 {justify-content:center;}.score-ring.svelte-10mivl5 {display:grid;place-items:center;width:9rem;height:9rem;border-radius:999px;font-size:2rem;font-weight:800;color:var(--color-base-content);background:color-mix(in oklab, var(--color-primary) 14%, transparent);border:4px solid color-mix(in oklab, var(--color-primary) 55%, transparent);box-shadow:0 0 28px color-mix(in oklab, var(--color-primary) 35%, transparent);}.result-text.svelte-10mivl5 {font-size:1.2rem;font-weight:600;color:color-mix(in oklab, var(--color-base-content) 80%, transparent);}.result-actions.svelte-10mivl5 {display:flex;gap:1rem;}\r\n\r\n    @media (max-width: 40rem) {.answers.svelte-10mivl5 {grid-template-columns:1fr;}\r\n    }'
};
function QuizPage($$anchor, $$props) {
  push($$props, true);
  append_styles($$anchor, $$css12);
  let params = prop($$props, "params", 7);
  let state3 = state(proxy({
    isLoading: true,
    errorMessage: "",
    user: null,
    stats: null,
    skills: [],
    courses: []
  }));
  onMount(() => {
    const unsubscribe = dashboardStore.subscribe((value) => {
      set(state3, value, true);
    });
    if (get2(state3).courses.length === 0) {
      dashboardStore.refresh();
    }
    return unsubscribe;
  });
  const courseTitle = user_derived(() => get2(state3).courses.find((course) => course.id === params()?.id)?.name ?? "HTML, beginners");
  const questions = [
    {
      prompt: "How do you start a HTML file?",
      options: [
        { text: "<html>", correct: true },
        { text: "<htm>", correct: false },
        { text: "<hml>", correct: false },
        { text: "<hm>", correct: false }
      ]
    },
    {
      prompt: "Which tag holds the page title?",
      options: [
        { text: "<title>", correct: true },
        { text: "<head>", correct: false },
        { text: "<h1>", correct: false },
        { text: "<meta>", correct: false }
      ]
    },
    {
      prompt: "Which tag creates a hyperlink?",
      options: [
        { text: "<a>", correct: true },
        { text: "<link>", correct: false },
        { text: "<href>", correct: false },
        { text: "<nav>", correct: false }
      ]
    },
    {
      prompt: "Which tag inserts an image?",
      options: [
        { text: "<img>", correct: true },
        { text: "<image>", correct: false },
        { text: "<src>", correct: false },
        { text: "<pic>", correct: false }
      ]
    },
    {
      prompt: "Which tag defines a list item?",
      options: [
        { text: "<li>", correct: true },
        { text: "<ul>", correct: false },
        { text: "<ol>", correct: false },
        { text: "<item>", correct: false }
      ]
    }
  ];
  const letters = ["A", "B", "C", "D"];
  let index2 = state(0);
  let selected = state(null);
  let score = state(0);
  let finished = state(false);
  let timer = null;
  const current = user_derived(() => questions[get2(index2)]);
  const answered = user_derived(() => get2(selected) !== null);
  const progressPct = user_derived(() => (get2(index2) + (get2(selected) !== null ? 1 : 0)) / questions.length * 100);
  function advance() {
    timer = null;
    if (get2(index2) === questions.length - 1) {
      set(finished, true);
    } else {
      set(index2, get2(index2) + 1);
      set(selected, null);
    }
  }
  function choose(optionIndex) {
    if (get2(selected) !== null) {
      return;
    }
    set(selected, optionIndex, true);
    if (get2(current).options[optionIndex].correct) {
      set(score, get2(score) + 1);
    }
    timer = setTimeout(advance, 950);
  }
  function restart() {
    set(index2, 0);
    set(selected, null);
    set(score, 0);
    set(finished, false);
  }
  onDestroy(() => {
    if (timer) {
      clearTimeout(timer);
    }
  });
  var $$exports = {
    get params() {
      return params();
    },
    set params($$value) {
      params($$value);
      flushSync();
    }
  };
  var div = root_45();
  var header = child(div);
  var button = child(header);
  var node = sibling(button, 2);
  {
    var consequent = ($$anchor2) => {
      var div_1 = root12();
      var div_2 = child(div_1);
      reset(div_1);
      template_effect(() => set_style(div_2, `width: ${get2(progressPct) ?? ""}%`));
      append($$anchor2, div_1);
    };
    if_block(node, ($$render) => {
      if (!get2(finished)) $$render(consequent);
    });
  }
  reset(header);
  var node_1 = sibling(header, 2);
  {
    var consequent_1 = ($$anchor2) => {
      var section = root_110();
      var h1 = child(section);
      var text2 = child(h1, true);
      reset(h1);
      var div_3 = sibling(h1, 2);
      var text_1 = child(div_3);
      reset(div_3);
      var p = sibling(div_3, 2);
      var text_2 = child(p, true);
      reset(p);
      var div_4 = sibling(p, 2);
      var button_1 = child(div_4);
      var button_2 = sibling(button_1, 2);
      reset(div_4);
      reset(section);
      template_effect(() => {
        set_text(text2, get2(courseTitle));
        set_text(text_1, `${get2(score) ?? ""}/${questions.length ?? ""}`);
        set_text(text_2, get2(score) === questions.length ? "Perfect! \u{1F389}" : "Nice work \u2014 keep practising!");
      });
      delegated("click", button_1, restart);
      delegated("click", button_2, () => push2("/"));
      append($$anchor2, section);
    };
    var alternate = ($$anchor2) => {
      var section_1 = root_36();
      var h1_1 = child(section_1);
      var text_3 = child(h1_1, true);
      reset(h1_1);
      var span = sibling(h1_1, 2);
      var text_4 = child(span);
      reset(span);
      var h2 = sibling(span, 2);
      var text_5 = child(h2, true);
      reset(h2);
      var div_5 = sibling(h2, 2);
      each(div_5, 23, () => get2(current).options, (option) => option.text, ($$anchor3, option, optionIndex) => {
        var button_3 = root_27();
        let classes;
        var span_1 = child(button_3);
        var text_6 = child(span_1, true);
        reset(span_1);
        var span_2 = sibling(span_1, 2);
        var text_7 = child(span_2, true);
        reset(span_2);
        reset(button_3);
        template_effect(() => {
          classes = set_class(button_3, 1, `answer c${get2(optionIndex) ?? ""}`, "svelte-10mivl5", classes, {
            correct: get2(answered) && get2(option).correct,
            wrong: get2(answered) && get2(optionIndex) === get2(selected) && !get2(option).correct,
            dim: get2(answered) && !get2(option).correct && get2(optionIndex) !== get2(selected)
          });
          button_3.disabled = get2(answered);
          set_text(text_6, letters[get2(optionIndex)]);
          set_text(text_7, get2(option).text);
        });
        delegated("click", button_3, () => choose(get2(optionIndex)));
        append($$anchor3, button_3);
      });
      reset(div_5);
      reset(section_1);
      template_effect(() => {
        set_text(text_3, get2(courseTitle));
        set_text(text_4, `Question ${get2(index2) + 1} / ${questions.length ?? ""}`);
        set_text(text_5, get2(current).prompt);
      });
      append($$anchor2, section_1);
    };
    if_block(node_1, ($$render) => {
      if (get2(finished)) $$render(consequent_1);
      else $$render(alternate, -1);
    });
  }
  reset(div);
  delegated("click", button, () => window.history.back());
  append($$anchor, div);
  return pop($$exports);
}
delegate(["click"]);
create_custom_element(QuizPage, { params: {} }, [], [], { mode: "open" });

// src/components/pages/ContentPage.svelte
var root13 = from_html(`<button type="button" class="toc-link svelte-uyhh09"> </button>`);
var root_111 = from_html(`<div class="content-screen svelte-uyhh09"><aside class="toc svelte-uyhh09"><button type="button" class="back svelte-uyhh09">\u2190 Back to chat</button> <p class="toc-label svelte-uyhh09">On this page</p> <nav class="toc-nav svelte-uyhh09" aria-label="Table of contents"></nav></aside> <main class="article svelte-uyhh09"><header class="article-head svelte-uyhh09"><p class="eyebrow svelte-uyhh09">Course content</p> <h1 class="article-title svelte-uyhh09"> </h1> <p class="placeholder-note svelte-uyhh09">\u{1F4DD} Sample content \u2014 the authored course material will appear here.</p></header> <section id="overview" class="block svelte-uyhh09"><h2 class="svelte-uyhh09">Overview</h2> <p>Welcome to <strong> </strong>. This page collects the course material in a
                readable, wiki-style format so you can browse concepts, examples and summaries at your own pace.</p></section> <section id="getting-started" class="block svelte-uyhh09"><h2 class="svelte-uyhh09">Getting started</h2> <p>Work through the sections in order. Each concept builds on the previous one.</p> <div class="callout svelte-uyhh09">\u{1F4A1} Tip: open the AI tutor (the chat icon) any time you want a concept explained differently.</div></section> <section id="key-concepts" class="block svelte-uyhh09"><h2 class="svelte-uyhh09">Key concepts</h2> <ul class="svelte-uyhh09"><li> </li> <li>How the pieces fit together in practice.</li> <li>Common mistakes and how to avoid them.</li></ul></section> <section id="example" class="block svelte-uyhh09"><h2 class="svelte-uyhh09">Example</h2> <p>A minimal example you can adapt:</p> <pre class="code svelte-uyhh09"><code> </code></pre></section> <section id="summary" class="block svelte-uyhh09"><h2 class="svelte-uyhh09">Summary</h2> <p> </p> <div class="actions svelte-uyhh09"><button type="button" class="btn btn-primary">Take the quiz</button> <button type="button" class="btn btn-ghost">Ask the tutor</button></div></section></main></div>`);
var $$css13 = {
  hash: "svelte-uyhh09",
  code: '.content-screen.svelte-uyhh09 {flex:1;min-height:0;overflow:hidden;display:grid;grid-template-columns:15rem minmax(0, 1fr);grid-template-rows:minmax(0, 1fr);width:100%;}\r\n\r\n    /* Sidebar stays put; it never scrolls. */.toc.svelte-uyhh09 {min-height:0;overflow:hidden;display:flex;flex-direction:column;gap:1rem;padding:1.5rem 1rem;border-right:1px solid color-mix(in oklab, var(--color-base-content) 10%, transparent);background:color-mix(in oklab, var(--color-base-100) 60%, transparent);}.back.svelte-uyhh09 {align-self:flex-start;background:none;border:none;cursor:pointer;font-weight:600;color:var(--color-primary);}.back.svelte-uyhh09:focus-visible {outline:2px solid var(--color-primary);outline-offset:2px;}.toc-label.svelte-uyhh09 {font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;color:color-mix(in oklab, var(--color-base-content) 55%, transparent);}.toc-nav.svelte-uyhh09 {display:flex;flex-direction:column;gap:0.15rem;}.toc-link.svelte-uyhh09 {text-align:left;padding:0.4rem 0.6rem;border-radius:0.5rem;border:none;background:transparent;color:color-mix(in oklab, var(--color-base-content) 75%, transparent);cursor:pointer;}.toc-link.svelte-uyhh09:hover {background:color-mix(in oklab, var(--color-primary) 14%, transparent);color:var(--color-base-content);}.article.svelte-uyhh09 {min-height:0;overflow-y:auto;padding:2.5rem 0;}\r\n\r\n    /* Content text spans ~90% of the content view. */.article.svelte-uyhh09 > :where(.svelte-uyhh09) {width:90%;margin-left:auto;margin-right:auto;}.article-head.svelte-uyhh09 {margin-bottom:2rem;padding-bottom:1rem;border-bottom:1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);}.eyebrow.svelte-uyhh09 {font-size:0.8rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--color-primary);}.article-title.svelte-uyhh09 {font-size:clamp(2rem, 4vw, 2.8rem);font-weight:800;color:var(--color-base-content);text-shadow:0 0 22px color-mix(in oklab, var(--color-primary) 30%, transparent);}.placeholder-note.svelte-uyhh09 {margin-top:0.5rem;font-size:0.85rem;color:color-mix(in oklab, var(--color-base-content) 60%, transparent);}.block.svelte-uyhh09 {margin-bottom:2.25rem;line-height:1.7;color:color-mix(in oklab, var(--color-base-content) 90%, transparent);}.block.svelte-uyhh09 h2:where(.svelte-uyhh09) {font-size:1.5rem;font-weight:700;margin-bottom:0.6rem;color:var(--color-base-content);}.block.svelte-uyhh09 ul:where(.svelte-uyhh09) {margin:0.5rem 0 0 1.25rem;display:flex;flex-direction:column;gap:0.35rem;}.callout.svelte-uyhh09 {margin-top:0.75rem;padding:0.9rem 1.1rem;border-radius:0.75rem;background:color-mix(in oklab, var(--color-primary) 12%, transparent);border-left:3px solid var(--color-primary);}.code.svelte-uyhh09 {margin-top:0.75rem;padding:1rem 1.25rem;border-radius:0.75rem;overflow-x:auto;font-family:ui-monospace, "SF Mono", Menlo, monospace;font-size:0.9rem;color:var(--color-base-content);background:color-mix(in oklab, var(--color-base-content) 8%, transparent);border:1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);}.actions.svelte-uyhh09 {display:flex;gap:0.75rem;margin-top:1rem;}\r\n\r\n    @media (max-width: 48rem) {.content-screen.svelte-uyhh09 {grid-template-columns:1fr;}.toc.svelte-uyhh09 {display:none;}\r\n    }'
};
function ContentPage($$anchor, $$props) {
  push($$props, true);
  append_styles($$anchor, $$css13);
  let params = prop($$props, "params", 7);
  let state3 = state(proxy({
    isLoading: true,
    errorMessage: "",
    user: null,
    stats: null,
    skills: [],
    courses: []
  }));
  onMount(() => {
    const unsubscribe = dashboardStore.subscribe((value) => {
      set(state3, value, true);
    });
    if (get2(state3).courses.length === 0) {
      dashboardStore.refresh();
    }
    return unsubscribe;
  });
  const courseTitle = user_derived(() => get2(state3).courses.find((course) => course.id === params()?.id)?.name ?? "Course");
  const sections = [
    { id: "overview", title: "Overview" },
    { id: "getting-started", title: "Getting started" },
    { id: "key-concepts", title: "Key concepts" },
    { id: "example", title: "Example" },
    { id: "summary", title: "Summary" }
  ];
  function scrollTo2(id) {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  var $$exports = {
    get params() {
      return params();
    },
    set params($$value) {
      params($$value);
      flushSync();
    }
  };
  var div = root_111();
  var aside = child(div);
  var button = child(aside);
  var nav = sibling(button, 4);
  each(nav, 21, () => sections, (section) => section.id, ($$anchor2, section) => {
    var button_1 = root13();
    var text2 = child(button_1, true);
    reset(button_1);
    template_effect(() => set_text(text2, get2(section).title));
    delegated("click", button_1, () => scrollTo2(get2(section).id));
    append($$anchor2, button_1);
  });
  reset(nav);
  reset(aside);
  var main = sibling(aside, 2);
  var header = child(main);
  var h1 = sibling(child(header), 2);
  var text_1 = child(h1, true);
  reset(h1);
  next(2);
  reset(header);
  var section_1 = sibling(header, 2);
  var p = sibling(child(section_1), 2);
  var strong = sibling(child(p));
  var text_2 = child(strong, true);
  reset(strong);
  next();
  reset(p);
  reset(section_1);
  var section_2 = sibling(section_1, 4);
  var ul = sibling(child(section_2), 2);
  var li = child(ul);
  var text_3 = child(li);
  reset(li);
  next(4);
  reset(ul);
  reset(section_2);
  var section_3 = sibling(section_2, 2);
  var pre = sibling(child(section_3), 4);
  var code = child(pre);
  var text_4 = child(code);
  reset(code);
  reset(pre);
  reset(section_3);
  var section_4 = sibling(section_3, 2);
  var p_1 = sibling(child(section_4), 2);
  var text_5 = child(p_1);
  reset(p_1);
  var div_1 = sibling(p_1, 2);
  var button_2 = child(div_1);
  var button_3 = sibling(button_2, 2);
  reset(div_1);
  reset(section_4);
  reset(main);
  reset(div);
  template_effect(() => {
    set_text(text_1, get2(courseTitle));
    set_text(text_2, get2(courseTitle));
    set_text(text_3, `The fundamentals and core vocabulary of ${get2(courseTitle) ?? ""}.`);
    set_text(text_4, `<!DOCTYPE html>
<html>
  <head><title>${get2(courseTitle) ?? ""}</title></head>
  <body>Hello, learner!</body>
</html>`);
    set_text(text_5, `You now have a map of ${get2(courseTitle) ?? ""}. Test yourself with the quiz, or ask the tutor to go deeper
                on any section.`);
  });
  delegated("click", button, () => push2(`/chat/${params()?.id ?? ""}`));
  delegated("click", button_2, () => push2(`/quiz/${params()?.id ?? ""}`));
  delegated("click", button_3, () => push2(`/chat/${params()?.id ?? ""}`));
  append($$anchor, div);
  return pop($$exports);
}
delegate(["click"]);
create_custom_element(ContentPage, { params: {} }, [], [], { mode: "open" });

// src/components/routes.ts
var routes_default = {
  "/": DashboardPage,
  "/profile": ProfileEditPage,
  "/chat/:id": CourseChatPage,
  "/quiz/:id": QuizPage,
  "/content/:id": ContentPage,
  "*": DashboardPage
};

// src/components/DashboardApp.svelte
var root14 = from_html(`<div><!> <main class="shell-content svelte-1w96du5"><!></main> <footer class="shell-footer svelte-1w96du5"><span>Copyright 2026 | OpenBook</span></footer> <!></div>`);
var $$css14 = {
  hash: "svelte-1w96du5",
  code: "\r\n    /* Lock the shell to the viewport so only inner page areas scroll. */.shell.svelte-1w96du5 {flex:1;height:100vh;min-height:0;overflow:hidden;display:flex;flex-direction:column;transition:padding-right 0.25s ease;}\r\n\r\n    /* Make room for the docked chat sidebar so nothing is hidden behind it. */.shell.chat-docked.svelte-1w96du5 {padding-right:min(28rem, 100vw);}.shell-content.svelte-1w96du5 {flex:1;min-height:0;overflow:hidden;display:flex;flex-direction:column;}.shell-footer.svelte-1w96du5 {margin-top:auto;padding:1rem 1.5rem 1.5rem;text-align:center;font-size:0.75rem;letter-spacing:0.08em;text-transform:uppercase;color:color-mix(in oklab, var(--color-base-content) 60%, transparent);border-top:1px solid color-mix(in oklab, var(--color-base-content) 10%, transparent);}"
};
function DashboardApp($$anchor, $$props) {
  push($$props, true);
  append_styles($$anchor, $$css14);
  let state3 = state(proxy({
    isLoading: true,
    errorMessage: "",
    user: null,
    stats: null,
    skills: [],
    courses: []
  }));
  let chatDocked = state(false);
  const onChatPage = user_derived(() => (router.location ?? "").startsWith("/chat"));
  onMount(() => {
    return dashboardStore.subscribe((value) => {
      set(state3, value, true);
    });
  });
  var div = root14();
  let classes;
  var node = child(div);
  DashboardHeader(node, {
    get user() {
      return get2(state3).user;
    }
  });
  var main = sibling(node, 2);
  var node_1 = child(main);
  Router(node_1, {
    get routes() {
      return routes_default;
    }
  });
  reset(main);
  var node_2 = sibling(main, 4);
  {
    var consequent = ($$anchor2) => {
      ChatWidget($$anchor2, { onSidebarChange: (docked) => set(chatDocked, docked, true) });
    };
    if_block(node_2, ($$render) => {
      if (!get2(onChatPage)) $$render(consequent);
    });
  }
  reset(div);
  template_effect(() => classes = set_class(div, 1, "shell svelte-1w96du5", null, classes, { "chat-docked": get2(chatDocked) && !get2(onChatPage) }));
  append($$anchor, div);
  pop();
}
create_custom_element(DashboardApp, {}, [], [], { mode: "open" });

// src/index.ts
initTheme();
mount(DashboardApp, { target: document.body });
//# sourceMappingURL=bundle.js.map
