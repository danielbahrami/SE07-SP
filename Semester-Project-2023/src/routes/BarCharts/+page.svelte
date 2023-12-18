<script lang="ts">

import { scaleBand, scaleLinear } from "d3";
import type { PageData } from '../$types';

// Declare the chart dimensions and margins.
export let data: PageData


const width = 800;
const height = 600;

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
    <svg {width} {height}>
      <g transform={`translate(${margin.left},${margin.top})`}>
        {#each xScale.ticks() as tickValue}
          <g transform={`translate(${xScale(tickValue)},0)`}>
            <line y2={innerHeight} stroke="White" />
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
    </svg>
</div>

  {#each data.vehicles as result}
      <h2>{result._id}</h2>
      <h2>{result.count}</h2>
  {/each}

<!--
<article>
  <h2>{data.vehicles}</h2>
</article>

-->
