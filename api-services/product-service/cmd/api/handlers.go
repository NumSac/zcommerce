package main

import "net/http"

var requestPayload struct {
	ProductId    string `json:"productId,omitempty"`
	CompanyId    string `json:"companyId,omitempty"`
	CategoryName string `json:"CategoryName,omitempty`
}

// Product specific handlers
// -----------------------
func (pr productsResource) handleProduct(w http.ResponseWriter, r *http.Request) {
}

func (pr productsResource) handleProductsByCategoryPaged(w http.ResponseWriter, r *http.Request) {

}

func (pr productsResource) handleProductsPaged(w http.ResponseWriter, r *http.Request) {

}

/// ----------------------

// Company specific handlers
// -------------------------
func (cr companyResource) handleCompany(w http.ResponseWriter, r *http.Request) {
}
func (cr companyResource) handleCompaniesByCategoryPaged(w http.ResponseWriter, r *http.Request) {
}
func (cr companyResource) handleCompaniesPaged(w http.ResponseWriter, r *http.Request) {
}
