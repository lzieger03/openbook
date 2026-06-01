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
An item within a breadcrumbs element.
-->

<script lang="ts">
	import type {Snippet} from "svelte";

	type Props = {
		href?:     string;
		class?:    string;
		target?:   string;
		rel?:      string;
		children?: Snippet;
	};

	let {
		href   = undefined,
        target = undefined,
		rel    = undefined,
		class: className = "",
		children,
	}: Props = $props();
</script>

<li class={className}>
	{#if href}
		<a {href} {target} {rel}>
			{@render children?.()}
		</a>
	{:else}
		{@render children?.()}
	{/if}
</li>
