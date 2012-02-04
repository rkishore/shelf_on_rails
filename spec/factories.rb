# By using the symbol ':user', we get Factory Girl to simulate the User model.
Factory.define :user do |user|
  user.name                  "Michael Hartl"
  user.email                 "mhartl@example.com"
  user.sex                   "Male"
  user.shirt_size            "Medium"
  user.pant_size             "Large"
  user.password              "foobar"
  user.password_confirmation "foobar"
end
