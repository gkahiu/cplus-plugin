import os

PRIORITY_LAYERS = [
    [
        {
            "uuid": "c931282f-db2d-4644-9786-6720b3ab206a",
            "name": "Carbon importance herding for health",
            "description": "Placeholder text for herding for health",
            "selected": True,
            "path": [],
        },
        {
            "uuid": "f5687ced-af18-4cfc-9bc3-8006e40420b6",
            "name": "Carbon importance eat fresh",
            "description": "Placeholder text for eat fresh",
            "selected": False,
            "path": [],
        },
    ],
    [
        {
            "uuid": "fef3c7e4-0cdf-477f-823b-a99da42f931e",
            "name": "Biodiversity herding for health",
            "description": "Placeholder text for herding for health",
            "selected": False,
            "path": [],
        },
        {
            "uuid": "fce41934-5196-45d5-80bd-96423ff0e74e",
            "name": "Biodiversity eat fresh",
            "description": "Placeholder text for eat fresh",
            "selected": False,
            "path": [],
        },
    ],
    [
        {
            "uuid": "3d69c1d6-8e0a-4bd0-ba55-0498e5d4ab1e",
            "name": "Test priority layer",
            "description": "Placeholder text for eat fresh",
            "selected": False,
            "path": [],
        },
    ],
]


PRIORITY_GROUPS = [
    {
        "uuid": "a4f76e6c-9f83-4a9c-b700-fb1ae04860a4",
        "name": "Carbon importance",
        "description": "Placeholder text for carbon importance",
    },
    {
        "uuid": "dcfb3214-4877-441c-b3ef-8228ab6dfad3",
        "name": "Biodiversity",
        "description": "Placeholder text for bio diversity",
    },
    {
        "uuid": "8b9fb419-b6b8-40e8-9438-c82901d18cd9",
        "name": "Livelihood",
        "description": "Placeholder text for livelihood",
    },
    {
        "uuid": "21a30a80-eb49-4c5e-aff6-558123688e09",
        "name": "Climate Resilience",
        "description": "Placeholder text for climate resilience ",
    },
    {
        "uuid": "ae1791c3-93fd-4e8a-8bdf-8f5fced11ade",
        "name": "Ecological infrastructure",
        "description": "Placeholder text for ecological infrastructure",
    },
    {
        "uuid": "8cac9e25-98a8-4eae-a257-14a4ef8995d0",
        "name": "Policy",
        "description": "Placeholder text for policy",
    },
    {
        "uuid": "3a66c845-2f9b-482c-b9a9-bcfca8395ad5",
        "name": "Finance - Years Experience",
        "description": "Placeholder text for years of experience",
    },
    {
        "uuid": "c6dbfe09-b05c-4cfc-8fc0-fb63cfe0ceee",
        "name": "Finance - Market Trends",
        "description": "Placeholder text for market trends",
    },
    {
        "uuid": "3038cce0-3470-4b09-bb2a-f82071fe57fd",
        "name": "Finance - Net Present value",
        "description": "Placeholder text for net present value",
    },
    {
        "uuid": "3b2c7421-f879-48ef-a973-2aa3b1390694",
        "name": "Finance - Carbon",
        "description": "Placeholder text for finance carbon",
    },
]

PWL_TEST_DATA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data",
    "priority",
    "layers",
    "test_priority_1.tif",
)

DEFAULT_PRIORITY_LAYERS = [
    {
        "type": "priority_layer",
        "layer_uuid": "7a9f87e6-ac58-4156-994d-b808ad0edf2d",
        "name": "Carbon Sequestration Potential CP norm",
        "size": 402164317,
        "layer_type": 0,
        "metadata": {
            "crs": "EPSG:4326",
            "unit": "degree",
            "is_raster": True,
            "resolution": [0.00898315284119522, 0.00898315284119522],
            "nodata_value": -9999.0,
            "is_geographic": True,
            "name": "CPLUS: Carbon Sequestration Potential CP norm",
            "description": "Carbon Sequestration Potential CP norm",
        },
        "filename": "Carbon Sequestration Potential CP norm",
        "path": PWL_TEST_DATA_PATH,
        "version": "2.0.0",
        "license": "Apache 2.0",
    }
]
