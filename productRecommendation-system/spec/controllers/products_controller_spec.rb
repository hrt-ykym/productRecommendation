require 'rails_helper'
require 'net/http'

RSpec.describe ProductsController, type: :controller do
  describe 'GET #index' do
    before do
      Product.destroy_all
      @product1 = Product.create(name: 'Product 1', description: 'Description 1', price: 10.0)
      @product2 = Product.create(name: 'Product 2', description: 'Description 2', price: 20.0)

      recommendations = [
        { 'id' => 1, 'name' => 'Product 3', 'description' => 'Description 3', 'price' => 30.0 },
        { 'id' => 2, 'name' => 'Product 4', 'description' => 'Description 4', 'price' => 40.0 },
        { 'id' => 3, 'name' => 'Product 5', 'description' => 'Description 5', 'price' => 50.0 }
      ]
      allow(Net::HTTP).to receive(:get).and_return(recommendations.to_json)

      ENV['FLASK_SERVICE_URL'] = 'http://localhost:5000'
    end

    it 'returns http success' do
      get :index
      expect(response).to have_http_status(:success)
    end

    it 'assigns @products' do
      get :index
      expect(assigns(:products)).to match_array([@product1, @product2])
    end

    it 'assigns @recommendations' do
      get :index
      expect(assigns(:recommendations).length).to eq(3)
    end

    it 'communicates with Flask app' do
      flask_response = Net::HTTP.get(URI(ENV['FLASK_SERVICE_URL'] + '/recommendations'))
      expect(flask_response).not_to be_nil
      parsed_response = JSON.parse(flask_response)
      expect(parsed_response.length).to eq(3)
    end
  end
end
