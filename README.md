# cistern

Wholesome CI metrics that can be visualised

### Building:

```
git clone https://github.com/KittyBorgX/cistern.git
cd cistern
cp example.env .env
# Fill out .env
python src/main.py
```

### What's this

A tool to parse the build output from the CI runner to give info such as build time per crate/section. Mainly intended for rust-lang/rust but can be used for other repositories as well.
