export interface searchJobDto {
  search?: string;
  workday?: string;
  minSalary?: string;
  location?: string;
  category?: number;
  company_id?: number;
  page?: number;
  per_page?: number;
}
