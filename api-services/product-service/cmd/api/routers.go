package main

import (
	"net/http"

	"github.com/go-chi/chi/v5"
)

// Product relataed operations will receive this
type productsResource struct{}

func (pr productsResource) Routes() http.Handler {
	r := chi.NewRouter()

	r.Get("/{productID}", pr.handleProduct)
	r.Get("/category/{categoryID:[0-9]+}", pr.handleProductsByCategoryPaged)
	r.Get("/", pr.handleProductsPaged)

	return r
}

// Company related operations will receive this
type companyResource struct{}

func (cr companyResource) Routes() http.Handler {
	r := chi.NewRouter()

	r.Get("/{companyID}", cr.handleCompany)
	r.Get("/category/{categoryID:[0-9]+}", cr.handleCompaniesByCategoryPaged)
	r.Get("/", cr.handleCompaniesPaged)

	return r
}
