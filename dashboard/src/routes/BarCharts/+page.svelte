<script lang="ts">

import { scaleBand, scaleLinear } from "d3";
import type { PageData } from '../$types';

// Declare the chart dimensions and margins.
export let data: PageData


const width = 1000;
const height = 700;

const margin = { top: 20, right: 20, bottom: 20, left: 180 };
const innerHeight = height - margin.top - margin.bottom;
const innerWidth = width - margin.left - margin.right;

$: xDomain = data.vehicles.map((d) => d._id);
$: yDomain = data.vehicles.map((d) => +d.count);

$: yScale = scaleBand().domain(xDomain).range([0, innerHeight]).padding(0.1);
$: xScale = scaleLinear().domain([0, 1000]).range([0,271257])
  .domain([0, Math.max.apply(null, yDomain)])
  .range([0, innerWidth]);

</script>

<div class="container mx-auto flex justify-center items-center">
    
    <svg {width} height="740" style="background-color:dimgray">
      <text x="200" y="16" class="heavy" fill="white">Bar Chart over most frequent manufactures invovled in collisions</text>

      <g transform={`translate(${margin.left},${margin.top})`}>
        {#each xScale.ticks() as tickValue}
          <g transform={`translate(${xScale(tickValue)},0)`}>
            <line y1="6" y2={innerHeight} stroke="white" />
            <text text-anchor="middle" dy=".71em" fill="White" y={innerHeight + 3}>
              {tickValue}
            </text>
          </g>
        {/each}
        {#each data.vehicles as d}
          <text
            text-anchor="end"
            fill="White"
            x="-3"
            dy=".32em"
            y={yScale(d._id) + yScale.bandwidth() / 2}
          >
            {d._id}
          </text>
          <rect
            x="0"
            fill="White"
            y={yScale(d._id)}
            width={xScale(d.count)}
            height={yScale.bandwidth()}
          />
        {/each}
      </g>
      <text x="2" y="370" class="small" fill="White">Manufactures</text>
      <text x="500" y="725" class="small" fill="white">Occurences</text>
    </svg>
</div>

<style>
.heavy {
  font: bold 20px sans-serif;
}

.small {
  font: italic 17px sans-serif;
}
</style>