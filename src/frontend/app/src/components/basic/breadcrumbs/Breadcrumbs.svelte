<!--
OpenBook: Interactive Online Textbooks
© 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
-->

<!--
@component
Breadcrumbs navigation line.
-->

<script lang="ts">
	import type {Snippet} from "svelte";

	type Props = {
		class?:    string;
		ulClass?:  string;
		children?: Snippet;
	};

	let {
		class: className = "",
		ulClass = "",
		children,
	}: Props = $props();
</script>

<div class={`breadcrumbs ${className}`.trim()}>
	<ul class={ulClass}>
		{@render children?.()}
	</ul>
</div>
