def user_listing_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/Listings/<filename>
    return 'user_{0}/Listings/{1}'.format(instance.seller.user.id, filename)