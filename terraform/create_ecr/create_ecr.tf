# 프로바이더 설정 : AWS Asia Pacific(Seoul)로 설정
provider "aws" {
  region = "ap-northeast-2"
}

/*
aws ecr에 관련된 similarity_scan API 이미지를 위한
drugvlab_llm_repository 리소스를 생성하고 강제 삭제 옵션을 true로 설정
*/
resource "aws_ecr_repository" "drugvlab_llm_repository" {
  name         = "drugvlab_llm"
  force_delete = true
}

/*
프로비저닝 리소스 수행 관리를 위해 사용되는 null_resource 형태의 push_drugvlab_llm_image 리소스
1. drugvlab_llm_repository.repository_url 이름의 도커 이미지를 삭제
2. ecr에 로그인
3. drugvlab_llm_repository.repository_url 태그의 도커 이미지 빌드
4. drugvlab_llm_repository.repository_url:latest 이미지 ecr에 push 

drugvlab_llm_repository 리소스가 생성된 후에만 실행 가능
*/
resource "null_resource" "push_drugvlab_llm_image" {
  provisioner "local-exec" {
    command = <<EOT
      cd ../../
      docker rmi -f ${self.triggers.repository_url} || true
      $(aws ecr get-login --no-include-email --region ${self.triggers.region} --registry-ids ${self.triggers.repository_id})
      docker build -t ${self.triggers.repository_url} -f Dockerfile .
      docker push "${self.triggers.repository_url}:latest"
    EOT
    environment = {
      AWS_DEFAULT_REGION = "ap-northeast-2"
    }
  }
  #drugvlab_llm_repository 리소스를 생성 하면서 만들어진 내용(repository_url, registry_id)를 사용
  #always_run을 통해 매 실행때마다 실행 되도록 보장
  triggers = {
    repository_url = aws_ecr_repository.drugvlab_llm_repository.repository_url
    repository_id  = aws_ecr_repository.drugvlab_llm_repository.registry_id
    region         = "ap-northeast-2"
    always_run     = "${timestamp()}"
  }

  depends_on = [aws_ecr_repository.drugvlab_llm_repository]
}
