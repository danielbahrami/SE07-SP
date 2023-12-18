import { COMBINED_SWITRS_COLLISIONS } from "$db/COMBINED_SWITRS_COLLISIONS"
import { SWITRS_PARTIES } from "$db/SWITRS_PARTIES"



/** @type {import('./$types').PageServerLoad} */
export const load: PageServerLoad = async () => {

	const projection = {_id:0, vehicle_make:1}

	//const vehicleOnly = await SWITRS_PARTIES.find({vehicle_make: {$not: {$eq: null}}}).project(projection).toArray()

	//const agreOnly = await SWITRS_PARTIES.aggregate([{$group : { _id : {vehicle_make:"$vehicle_make"}, count : {$sum : 1}}}]).toArray()

	// const result = await SWITRS_PARTIES.aggregate([{$sortByCount: "$vehicle_make"}]).toArray()
	
	const result = await SWITRS_PARTIES.aggregate([
				{ $match: {
					vehicle_make: { 
						$exists: true, 
						$ne: null 
					}
				} },
				{ $group: {
					_id: 
						"$vehicle_make"
					,
					count: { $sum: 1 }
				} },
				{ $sort: { count: -1 } }   
			]).toArray();

	const result1 = result.slice(0, 10)

	//const data = JSON.parse(JSON.stringify(result1))

	//const serilizedData1 = JSON.stringify(result1)

	//console.log(data)
	return {
		vehicles : result1
	}

}

