# JSON-Entity-Cloning
A METHOD TO CLONE AN ENTITY AND ALL ITS RELATED ENTITIES

An Entity is defined as a structure with the following three fields:

	1.ID
	2.Name
	3.Description (optional)

Related Entities are represented as links from one Entity to another. A link entry has the following fields:

	1.From Entity ID
	2.To Entity ID

Note: Links are directional, i.e. they go from one entity to another. You can think of this as a directed graph where Entities are the vertices and the Links are edges.

SPECIFICATIONS:
The program takes in as an input a JSON file representing the entities and the links in the system and the id of the entity that needs to be cloned.

	python assignment.py <json_input_file_name> <entity_id>
  
The JSON file contains the following information:

	1. entities: A list of all the entities in the system. One can assume that the ids are unique integers.
	2. links: a list of all the links in the system

The format of the JSON file is as follows:

	{
		"entities": [{
			"entity_id": 3,
			"name": "EntityA"
		}, {
			"entity_id": 5,
			"name": "EntityB"
		}, {
			"entity_id": 7,
			"name": "EntityC",
			"description": "More details about entity C"
		}, {
			"entity_id": 11,
			"name": "EntityD"
		}],
		"links": [{
			"from": 3,
			"to": 5
		}, {
			"from": 3,
			"to": 7
		}, {
			"from": 5,
			"to": 7
		}, {
			"from": 7,
			"to": 11
		}]
	}

After reading the json file the program does the following:

	1. Finds the entity with the entityid given as a parameter on the command line. This is referred to as the initial entity below.
	2. Creates a clone (copy) of the initial entity and assigns it a new id(next greater than the max available id)
	3. Clones all the related entities by traversing the links from the initial entity. This process continues till all the related entities and links have been cloned. Note there may be loops in entities, i.e. an entity may link back to one of its ancestors.
	4. For the initial entity, any entities that link to it now also link to the clone of the initial entity.
	5. All the new entities and links have been added back to the list of entities and links.
	6. When the cloning is completed, the program output is the entities and links to standard output as valid JSON in the same format as the input file.
EXAMPLE:
For the input file shown above, and entity_id to clone as 5, the expected output is as follows: (Note: order of entities and links does not matter. The ids assigned to the cloned entities does not matter, as long as they are unique.)

Output:

	{
		"entities": [{
			"entity_id": 3,
			"name": "EntityA"
		}, {
			"entity_id": 5,
			"name": "EntityB"
		}, {
			"entity_id": 7,
			"name": "EntityC",
			"description": "More details about entity C"
		}, {
			"entity_id": 11,
			"name": "EntityD"
		}, {
			"entity_id": 13,
			"name": "EntityB"
		}, {
			"entity_id": 17,
			"name": "EntityC",
			"description": "More details about entity C"
		}, {
			"entity_id": 19,
			"name": "EntityD"
		}],
		"links": [{
			"from": 3,
			"to": 5
		}, {
			"from": 3,
			"to": 7
		}, {
			"from": 5,
			"to": 7
		}, {
			"from": 7,
			"to": 11
		}, {
			"from": 3,
			"to": 13
		}, {
			"from": 13,
			"to": 17
		}, {
			"from": 17,
			"to": 19
		}]
	}
