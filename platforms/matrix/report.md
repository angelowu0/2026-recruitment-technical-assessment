# Matrix Assessment Report

> [!TIP]
> Use this document to record your progress, the problems you faced and how you solved (or avoided) them.
> You can include images or add files in this directory if you want.

Followed Tuwunel guide using Caddy docker-compose file:

Pulling docker image
401 error failed to fetch oauth token-I, had to verify my email through docker

Buy domain and set dns to cloudflare’s dns servers

Setup cloudflare tunnel after login

Ran the docker container using he provided compose file and couldn't connect client, so checked error logs for caddy and
saw that i had an error 403 which caddy couldn't get a certificate from let-encrypt andthen saw I was rate limited, I had
to change to DNS certification

I ran into a problem where Cloudflare tunnel seems to be refused every ip address and was unable to resolve this issue:
I tried:
- using traefik as a reverse proxy
- using caddy
- not using a reverse proxy
- adding various application routes to cloudflare tunnel

## Matrix Handle

<!-- TODO: Replace with your matrix handle -->
`@example:example.com`
