function out = read_cctv_frame(filename)
tmp=fread(fopen(filename,'r'));
out=demosaic( reshape(uint8(tmp),[752,560])','grbg');