<script lang="ts">
	import * as d3 from 'd3';
	import californiaMap from '$lib/map/California_County_Boundaries.json';
	import { draw } from 'svelte/transition';

	export let data: PageData;

	let width = 900;
	let height = 900;

	let selected;

	/* Usefull for potentially later other data vizs
const xScale = d3.scaleLinear()
    .domain([d3.min(data.coordinates, d => d.latitude), d3.max(data.coordinates, d => d.latitude)])
    .range([0, width])

const yScale = d3.scaleLinear()
    .domain([d3.min(data.coordinates, d => d.longitude), d3.max(data.coordinates, d => d.longitude)])
    .range([height, 0])
*/

	let projection = d3.geoEquirectangular().fitSize([width, height], californiaMap);

	let geoGenerator = d3.geoPath().projection(projection);

	const points = data.coordinates.map((p) => projection([p.longitude, p.latitude]));
</script>

<div class="container mx-auto flex justify-center items-center">
	<svg xmlns="http://www.w3.org/2000/svg" {width} {height} style="background-color:dimgray">
		<text x="200" y="25" class="heavy" fill="white">Map over collisions in Carlifornia</text>

		<rect x="1" y="450" width="80" height="50" stroke="white" fill="transparent" stroke-width="2" />
		<circle cx="10" cy="465" r="2" stroke="black" fill="black" />
		<text x="16" y="470" class="small" fill="white">Collision</text>
		<text x="16" y="485" class="small" fill="white">Point</text>

		<g fill="white" stroke="black">
			{#each californiaMap.features as feature, i}
				<path
					d={geoGenerator(feature)}
					on:click={() => (selected = feature)}
					class="county"
					in:draw={{ delay: i * 50, duration: 1000 }}
				/>
			{/each}
		</g>

		{#if selected}
			<path d={geoGenerator(selected)} fill="hsl(0 0% 50% / 20%)" stroke="black" stroke-width={2} />
		{/if}

		{#each points as [cx, cy]}
			<circle {cx} {cy} r="1" stroke="black" fill="black" />
		{/each}
	</svg>
</div>

<div class="selectedName">County: {selected?.properties.CountyName ?? ''}</div>

<style>
	.county:hover {
		fill: hsl(0 0% 50% / 20%);
	}

	.selectedName {
		text-align: center;
		margin-top: 8px;
		font-size: 1.5rem;
	}

	.heavy {
		font: bold 30px sans-serif;
	}

	.small {
		font: italic 13px sans-serif;
	}
</style>
