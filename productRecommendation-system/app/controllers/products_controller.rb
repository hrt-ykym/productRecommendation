require 'net/http'

class ProductsController < ApplicationController
  def index
    @products = Product.all

    uri = URI('http://localhost:5000/recommendations')
    response = Net::HTTP.get(uri)
    @recommendations = JSON.parse(response)

    render json: { products: @products, recommendations: @recommendations }
  end
end
