require 'net/http'

class ProductsController < ApplicationController
  def index
    @products = Product.all

    uri = URI('http://localhost:5000/recommendations')
    response = Net::HTTP.get(uri)
    @recommendations = JSON.parse(response)

    respond_to do |format|
      format.html  # index.html.erbを表示
      format.json { render json: { products: @products, recommendations: @recommendations } }
    end
  end

  def show
    @product = Product.find(params[:id])
    render json: @product
  end
end
