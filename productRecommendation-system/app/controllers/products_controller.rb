require 'net/http'

class ProductsController < ApplicationController
  def index
    @products = Product.all

    uri = URI('http://localhost:5000/recommendations')
    response = Net::HTTP.get(uri)
    @recommendations = JSON.parse(response)

    @data = { products: @products, recommendations: @recommendations }

    render json: @data
  end

  def show
    @product = Product.find(params[:id])
    render json: @product
  end
end
