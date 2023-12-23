import { SWITRS_PARTIES } from '$db/SWITRS_PARTIES';

/** @type {import('./$types').PageServerLoad} */
export const load: PageServerLoad = async () => {
	const result = await SWITRS_PARTIES.aggregate([
		{
			$match: {
				vehicle_make: {
					$exists: true,
					$ne: null
				}
			}
		},
		{
			$group: {
				_id: '$vehicle_make',
				count: { $sum: 1 }
			}
		},
		{ $sort: { count: -1 } }
	]).toArray();

	const result1 = result.slice(0, 10);

	return {
		vehicles: result1
	};
};
