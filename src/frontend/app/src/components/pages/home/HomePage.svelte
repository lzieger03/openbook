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
Placeholder for the start page until we have proper content to show.
 -->
<script lang="ts">
	import Card        from "../../basic/card/Card.svelte";
	import CardActions from "../../basic/card/CardActions.svelte";
	import CardBody    from "../../basic/card/CardBody.svelte";
	import CardHeader  from "../../basic/card/CardHeader.svelte";
	import CardSubtitle from "../../basic/card/CardSubtitle.svelte";
	import CardTitle   from "../../basic/card/CardTitle.svelte";
</script>

<div class="flex-1 flex flex-col items-center justify-center bg-base-200">
	<Card variant="elevated" class="w-full max-w-xl">
		<CardBody class="items-center text-center">
			<CardHeader class="items-center gap-4">
				<CardTitle class="text-4xl font-bold text-primary">OpenBook</CardTitle>
				<CardSubtitle class="text-lg text-base-content/80">
					Interactive Online Textbooks
				</CardSubtitle>
			</CardHeader>

			<div class="avatar mb-2">
				<div class="flex w-24 items-center justify-center rounded-full bg-primary/10 ring ring-primary ring-offset-2 ring-offset-base-100">
					<span class="text-5xl text-primary">📚</span>
				</div>
			</div>

			<div class="alert alert-info shadow-lg">
				<span>
					Welcome to OpenBook! This is a placeholder for the start page until we have proper content to show.
				</span>
			</div>

			<CardActions justify="center" class="w-full">
				<button class="btn btn-primary btn-wide" disabled>
					Get Started (Coming Soon)
				</button>
			</CardActions>
		</CardBody>
	</Card>
</div>
