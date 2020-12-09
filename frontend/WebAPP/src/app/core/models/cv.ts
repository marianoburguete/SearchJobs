export interface cv {
    id?: number;
    name?: string;
    birth_date?: string;
    phone?: string;
    country?: string;
    address?: string;
    avatar?: string;
    description?: string;
    education?: education[];
    workexperience?: workexperience[];
    languages?: language[];
    categories?: category[];
    user?: {
        id?: number;
        email?: string;
    }
}

export interface education {
    name?: string;
    place?: string;
    start_date?: string;
    end_date?: string;
}

export interface workexperience {
    name?: string;
    ocupation?: string;
    start_date?: string;
    end_date?: string;
}

export interface language {
    name?: string;
}

export interface category {
    category?: {
        id?: number;
        name?: string;
    };
}