<script lang="ts">
	import '../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';
</script>

<!-- App Shell -->
<AppShell>
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar>
			<svelte:fragment slot="lead">
				<strong class="text-xl uppercase">Scalable Systems Project - Group 15</strong>
			</svelte:fragment>
			<svelte:fragment slot="default">
				<a
					class="btn btn-sm variant-ghost-surface"
					href="/BarCharts"
					target="_self"
					rel="noreferrer"
				>
					Bar Charts
				</a>	
				<a
					class="btn btn-sm variant-ghost-surface"
					href="/MapChart"
					target="_self"
					rel="noreferrer"
				>
					Map Chart	
				</a>
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<!-- Page Route Content -->
	<slot />
</AppShell>
