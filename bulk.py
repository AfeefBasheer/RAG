import requests
from concurrent.futures import ThreadPoolExecutor


JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDAwIiwidGVuYW50X2lkIjoiMDAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDAxIiwicm9sZSI6InVzZXIiLCJleHAiOjE3NzgwODU1NDEsImlhdCI6MTc3ODA4MTk0MX0.55Gc8c61l3y-kD9nmigda-_zn1enq7y-2M6UhHtFSwA"

HEADERS = {
    "Authorization": f"Bearer {JWT_TOKEN}"
}
INGEST_URL = "http://127.0.0.1:8000/ingest"

document_ids = [
    "f72f7514-889f-4afd-96b3-2a0132acf86f",
    "43f14c8e-834c-4c21-a5e5-f47c1c067c8d",
    "042e6bcd-98d4-4448-8c09-c0b5e8c5bea6",
    "ed5f443d-a794-4f0d-9031-13564290d32b",
    "597ce7a8-ab58-4821-9779-7fdb06550e50",
    "b37adf39-3280-405b-8743-48af7b0f4785",
    "6cbc4cba-2170-46e7-89d3-28e1f6ac433f",
    "160dedc3-8a11-45c5-8d96-7eca8ef3d46a",
    "07163ed2-daf4-463d-8e70-e8d5a36aac0c",
    "7a28020d-5457-4827-b82b-729fd807a38d",
    "e3b950bc-38e1-4280-97e6-0855d87f2a82",
    "c541d13b-fd11-4be0-92c4-77eaafe1984e",
    "4e6f32c6-d173-4897-88ca-b31267a8867d",
    "1f56e939-99ee-40ce-9b32-6352606bfb12",
    "081cdeb0-133f-4ab0-aed7-28d785aa58d4",
    "a6ae72b2-0bb2-46af-8eff-dbaccf67bf6d",
    "61be2972-2b98-409d-b8e8-3dbffc2f5948",
    "1ef5da86-9d92-4e6d-a1cb-4b5ebbb86183",
    "b95f441b-d8b7-4793-9b6b-371ea816ea9a",
    "33c10c83-6fc4-4564-a606-77a6125c9e32",
    "3c6e817f-0de1-4111-91de-c9aa9a3aca03",
    "218ac401-690a-411f-8026-57a675904e92",
    "6d078a76-84b6-43f1-9305-b89bb70829bb",
    "8e51db89-a19a-4eb3-ae11-398a761f875e",
    "395230b3-2b33-4a0c-b69f-70f4bbc80ad0",
    "1817416c-7f2d-488d-8932-dbe12a5a668f",
    "b56f552c-6db1-473f-af99-2e6f761931a2",
    "52d93bcc-380e-4664-abb6-c058d3d13cbe",
    "1f37d0d0-9b44-4ccb-a856-3888f4604575",
    "7254f575-a7e7-411b-92e2-392ed9350857",
    "8a1a7317-1979-4e22-9629-c2e0dfb2a40e",
    "e2d711d8-c733-4e1d-a045-3ae578bc7e2f",
    "6bcbc45f-9433-4f98-b3d7-906aa8cdb29c",
    "2af44091-060a-474f-8273-776ff81610d3",
    "352d9c45-b3a4-4365-bff0-b3100a5ebd0d",
    "7e772b16-cd1e-4367-9834-c52f8ca459f0",
    "41ab23f4-c01e-4c78-b294-ba00c2f8759b",
    "4e84c88e-877d-494b-86d5-6c32b65d4824",
    "a8a7ebfe-4579-445b-b564-fcc51b8a9477",
    "4b393d23-07b1-401b-9bb2-03a542ea7464",
    "6978b54f-6b29-407e-b447-80bb667189f3",
    "7df6a635-5899-41f1-8300-f6335fd69811",
    "36788539-5c20-4e5e-8389-dd8badbcd4de",
    "6651c12d-99fe-45a1-ad36-2eea4f0541e6",
    "2a4bfa1f-4444-4faa-ac84-b0fca4e6233d",
    "209eac27-d5a7-487e-a2c4-aa5bd6a4e1bc",
    "67ea050e-9141-4d78-bd47-331fdb2f31f4",
    "372c3791-1a8d-473f-b721-6536b2d685c8",
    "2646897b-3912-44bf-bd4b-713d118b41ad",
    "26f38f5c-b76f-44c8-acd6-014617feb4d6",
    "e653bc8b-7d8d-463f-940c-738ba522bcd3",
    "ef0b964b-cecd-4503-b126-faa8dc2a5034",
    "b07955d9-4cc9-4721-ae91-a62adc70088d",
    "f82ab7a2-363e-4921-b5a4-843a98bd177f",
    "bc5c0663-8caa-4a5a-8d59-19718bb87847",
    "ff149d8c-340d-4122-89e7-57010c85bb75",
    "abdb5123-09ef-4937-a011-1cd4b8ccb180",
    "51f06971-03ad-46ed-8950-46c689e48538",
    "e404b32b-36e5-4f41-9d88-a39664fd64a8",
    "5a8622c2-cd05-4c54-938a-636a44ab0d84",
    "fba4e065-5f00-4ea1-90d8-a9d6d77369e7",
    "d946e505-70d0-45ae-b5c4-72f34e7b552c",
    "41672d6c-eb06-4ee9-be46-0d6418d615d4",
    "8591bf51-a3e2-40bc-b2c5-c7d4f280908f",
    "799a94f4-b501-43b2-88ac-28e248456ef7",
    "72889f98-72ea-4b0f-bdba-d39e8c16be15",
    "581aba7f-fb8e-413a-b1cd-989045a2fa30",
    "b4e6be53-829a-4a04-b2ec-a7ddbe01519b",
    "073cf54b-bbcb-4942-a039-3bc688032a21",
    "8aa737ea-e59a-4bba-a397-a8d2889f033b",
    "e0b93cb2-3722-4911-b177-ee3e461ce420",
    "031b29d5-d13f-4568-bcb1-ef211d4f903e",
    "aa7a32c7-df84-42f4-a61a-4718a1b163e8",
    "e5c54221-a8bb-4930-962d-57f311447a5d",
    "913b6980-c6ea-498f-80c5-d9def5141c0c",
    "be3c4f67-cefa-495e-87e9-69e30a8c1b91",
    "3d3953f6-c6ec-4909-8db6-b9887a51e568",
    "4d4a7e28-c003-4807-a8b4-036ed51e2bdf",
    "1f91967e-eef2-4794-b2a7-229ebf8a9e5c",
    "c9b4bb59-8d0b-4b62-b9eb-8297437a04c7",
    "5be1a666-5326-40eb-93a7-49d067ec88e5",
    "583bcbd6-a989-45ec-ac65-749526b97dab",
    "fbfd76d5-94a2-48a9-bb57-208ede5f4907",
    "a7a5e827-377c-4b4f-8c3b-8701a5616f0a",
    "e17afd3a-1d24-4f06-bdf0-bb851a91d453",
    "b889a752-83d8-4c08-a9a4-8a2722a0bc78",
    "0ba4344c-1259-4dc4-b9dd-9b9944592d5e",
    "4589e79b-522e-44e4-9a75-ee7d0e414a93",
    "41d7f9d7-4935-45d3-89d9-8b6563cf0516",
    "c961d6a7-2286-4194-aafb-c4bff28e3a6d",
    "b4e2be8a-b409-4fe7-8285-1d1cc9d76f5c",
    "ae1a991d-33a1-42a9-864d-dc11b63ecac4",
    "fcedfbd5-f0c8-45bf-b84a-bb7465638145",
    "2391889a-7911-4e8e-a8b0-13ec2fd38db3",
    "781d0b19-e45a-4fe3-b72a-4720032e0587",
    "e7b86d1f-0fb9-4c37-a5a3-ae10b7f2683c",
    "d915c143-95de-4c25-9ea3-74cdf07f5eab",
    "e3c24a4c-c7ba-477e-8d64-67eb2cab9962",
    "ecc7cd1a-f814-402c-9ccb-cff3a5418ab2",
    "62be972a-50bd-46bc-bc49-e55759b56426"
]


def ingest_document(document_id):
    try:
        response = requests.post(
            f"{INGEST_URL}/{document_id}",
            headers=HEADERS
        )

        print(document_id, response.status_code)

    except Exception as e:
        print(document_id, e)


with ThreadPoolExecutor(max_workers=100) as executor:

    futures = [
        executor.submit(ingest_document, doc_id)
        for doc_id in document_ids
    ]

    for future in futures:
        future.result()