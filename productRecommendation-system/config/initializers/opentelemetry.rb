# config/initializers/opentelemetry.rb
require 'opentelemetry/sdk'
require 'opentelemetry/instrumentation/all'

OpenTelemetry::SDK.configure do |c|
  c.service_name = ENV['OTEL_SERVICE_NAME'] || 'rails-app'
  c.use_all() # enables all instrumentation!
end
