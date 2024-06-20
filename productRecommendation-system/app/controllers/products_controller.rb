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
  end
  