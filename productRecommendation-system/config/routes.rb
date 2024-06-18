Rails.application.routes.draw do
  resources :products, only: [:index, :show]
  root 'products#index'
end