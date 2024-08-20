def login_parse_handler(soup):
    param = soup.find(name="meta", attrs={"name": "csrf-param"})["content"]
    token = soup.find(name="meta", attrs={"name": "csrf-token"})["content"]
    
    submit = soup.find(name="input", attrs={"type": "submit"})
    submit_name, submit_value = submit["name"], submit["value"]
    
    login_name = soup.find(name="input", attrs={"id": "user_username"})["name"]
    passwrod_name = soup.find(name="input", attrs={"id": "user_password"})["name"]
    
    return (
        param, 
        token, 
        submit_name, 
        submit_value, 
        login_name, 
        passwrod_name
        )