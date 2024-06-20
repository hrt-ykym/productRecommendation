Rails.application.routes.draw do
  resources :products, only: [:index, :show, :new, :create] do
    collection do
      get 'api', to: 'products#api_index'
    end
  end
  root 'products#index'
end
