from locust import HttpUser, SequentialTaskSet, between, task

"""
Cookies are used to let the server "remember" the client connection and state, then respond based on those client IDs.

Cookie flow
1. Client sends a request                     ------------request---------->  Server receives it 
2. Client receives the response and a cookie  <---------resp & cookie-------  Server responds and sends a cookie
3. Client store the cookie
4. Client sends the request and cookie         -----request & cookie------->  Server receives the cookie and nkows who is the client
5. Client receive the reponse                  <----------Response----------  Server sends the reponse (send a cookie only if a new one is required)

To access variables across different tasks, we need to create an __init__ method and define a self.<var_name>
"""

class UserBehaviour(SequentialTaskSet):
    
    def __init__(self, parent):
        super().__init__(parent)
        self._session_id = ""
        self.ajs_user_id = ""
    
    def on_start(self):
        print("I will lauch URL")
        res = self.client.get("/login", name="Get_URL")
        self._session_id = res.cookie["_session_id"]
        print(f"I will retrieve cookie --> {self._session_id}")
        print("I will login + using cookie")
        with self.client.post("/login", name="LogIn", catch_response=True, cookie={"_session_id": self._session_id}, data={
            "captcha_token": "03AGdBq24miaFpgcKv5WSQF5Otg_-N51PCrqHBaWZNRfAgpAUmbVdxy_62RcWYoJGA4Sx0Zvvqst9P5sJ4q_ozynbHbGQaujaayZbvJ-oioBfdiluuYnFyRC56Zws-dcWIidN_iuseAzAL803FMrV2Q54ymt-NDbgDtGvDKOQlAz4IhtalPB2wbaaaYaF858e4SlLo3AFxJvshKzjmw2Zzl7g4K2Y_4GBZ_zdAy-aTPDwFNIPzWoNJBPXvoZbJ4nvxkV13X7RqTOrJTjnosozT7jdcgTCHDN8e5II35DMCBHV0gI_0bFK_RlXvnOsVHP_BzBnwI79QHMXer12JTnbijuTNbuo1u0DwTzHna-uzA_X6FdYTUkJt54WMxlekHawNI9mOUt-D1D4EuUUFScvvAmcVxN5vUHveilE9tk10bTNT3Sz318NE3EpG8-cpLf6qVQhQNMpn0QH_",
            "captcha_version": "v3",
            "user[login]": "",
            "user": {
                "login": "yermy.ar@gmail.com",
                "password": "Ingram1234."
            },
            "redirect": None,
            "authenticity_token": "lnAG4tbuaCK+tbCDH7UahNj31idcHUfUYapqTEOlNqFeH6VaAB+rbaSAPFMJHPM4Z5xrGUQtoWjOILINo86EHg=="
        }) as post_resp:
            if post_resp.status_code == 200:
                post_resp.success()
            else:
                post_resp.failure("Failed to login")
    
    @task
    def select(self):
        print(f"using 2 cookies: code academy _session_id -> {self._session_id} and PYTHON")

class MyUser(HttpUser):
    tasks = [UserBehaviour]
    wait_time = between(2, 4)
    host = "https://www.codecademy.com"
