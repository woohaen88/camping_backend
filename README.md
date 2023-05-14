API : 
    GET POST api/v1/camping/
    GET PUT PATCH DELETE api/v1/camping/1

    POST api/v1/user/signup   --> 회원가입

    

[Model]
    CampGround
        - relation:
            [FK] owner: int
            [M2M] tags: int[]

        - columns:
            price: int
            address: str
            description: str | null            
            pet_friendly: boolean, default=False
            ev_friendly: boolean, default=False
            check_in: date
            check_out: date
            ratings: int
            name: str

    Tag
        - columns:
            name: str
            slug: str, auto


[API List]
Login  
Signup  
    - google로 로그인  
    - kakao로 로그인
