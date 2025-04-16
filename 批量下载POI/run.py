from 批量下载POI.DownLoader import BaiduDownLoader, BaseDownLoader

if __name__ == '__main__':
    down_loader = BaiduDownLoader(ak="ak")
    # down_loader.set_params(BaiduDownLoader.Param.PageNum,6)
    down_loader.set_params(BaiduDownLoader.Param.Region, BaiduDownLoader.Region.AnQing)
    down_loader.download(BaiduDownLoader.KeyWord.Company)
    down_loader.save_to_csv("company")