class ProductsController < ApplicationController
  require 'net/http'
  require 'uri'
  require 'json'

  def index
    @products = Product.all
    flask_service_url = ENV['FLASK_SERVICE_URL'] || 'http://recommendationengine:5000'
    uri = URI("#{flask_service_url}/recommendations")
    begin
      response = fetch_recommendations(uri)
      @recommendations = JSON.parse(response)
    rescue => e
      Rails.logger.error("Error fetching recommendations: #{e.message}")
      @recommendations = [{'name' => 'Recommendation error', 'description' => 'Unable to fetch recommendations at this time.', 'price' => 'N/A'}]
    end

    respond_to do |format|
      format.html  # index.html.erbを表示
      format.json { render json: { products: @products, recommendations: @recommendations } }
    end
  end

  def show
    @product = Product.find(params[:id])
    render json: @product
  end

  def new
    @product = Product.new
  end

  def create
    @product = Product.new(product_params)
    if @product.save
      redirect_to products_path, notice: 'Product was successfully created.'
    else
      render :new
    end
  end

  def api_index
    @products = Product.all
    render json: @products
  end

  private

  def product_params
    params.require(:product).permit(:name, :description, :price)
  end

  def fetch_recommendations(uri)
    http = Net::HTTP.new(uri.host, uri.port)
    http.open_timeout = 5
    http.read_timeout = 5

    request = Net::HTTP::Get.new(uri.request_uri)
    response = http.request(request)
    response.body
  end
end
