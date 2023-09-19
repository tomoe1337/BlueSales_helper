import vk_api


vk_session = vk_api.VkApi(token = 'vk1.a.IitNQRC0AmE4MKK7vESqoOwt5IMwuEwDFFLQNU9PSHt-QgmkmaZu8hHI2sS07ju8pGANInxJ0dJ2og-CtRXD42W-dPlxkoIUrG88fVZ_-msgcF6axf-Au3Xr66qbOtXeqaEAfG4qQfk0wIl9E92FAjYHygc8jN6SCccOduiPnTH1rYaJPm2Hclci5GyXQA1FsrK1FmEm67NvTY6EHpbGzA')
vk = vk_session.get_api()
print(vk.users.get(user_ids = 'https://vk.com/zxcinsanexd')[0]['id'])