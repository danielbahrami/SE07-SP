import { COMBINED_SWITRS_COLLISIONS } from "$db/COMBINED_SWITRS_COLLISIONS"

/** @type {import('./$types').PageServerLoad} */
export const load: PageServerLoad = async () => {

	const projection = {_id:0, longitude:1, latitude:1}

	const res = await COMBINED_SWITRS_COLLISIONS.find({longitude: { $ne: null}, latitude: { $ne: null}}).project(projection).toArray();

    const result = res.slice(0, 10000)

	return {
        coordinates : result
    }

}

